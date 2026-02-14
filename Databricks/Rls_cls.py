
from dataclasses import dataclass
from enum import Enum
from typing import List, Set
import logging

from pyspark.sql import Row

from sap_api.config.common import get_config, get_spark


logger = logging.getLogger(__name__)


class SecurityType(Enum): #twardy hard, sa tylko dwie opcje filtrow.
    RLS = "rls"
    CLS = "cls"


@dataclass
class SecurityConfig:
    catalog: str
    schema: str


@dataclass
class SecurityPolicy:
    security_type: SecurityType
    table_name: str
    function_name: str
    column_name: str = None


class DatabricksSecurityManager:
    def __init__(self, config):
        self.spark = get_spark()
        self.config = config # config z srodowsika, zawiera katalog i schemat
        self.security_config = SecurityConfig(
            catalog=config.uc.catalog_name, schema=config.uc.schema_name
        )
        self.spark.sql(f"USE CATALOG {self.security_config.catalog}")

    def _get_tables(self) -> List[Row]:
        """Retrieve all tables from schema."""
        logger.debug("Retrieving tables from schema")
        return self.spark.sql(
            f"SHOW TABLES IN {self.security_config.catalog}.{self.security_config.schema}"
        ).collect()

    def _get_table_tags(self) -> List[Row]: # pobierz tagi z tabeli, które są przypisane do tabel, a nie do kolumn. Pobieramy z tabel systemowych. Oby nie byly filtroawne - sprawdzic
        """Retrieve table-level security tags."""
        logger.debug("Retrieving table-level security tags")
        return self.spark.sql(
            f"""SELECT * FROM {self.security_config.catalog}.information_schema.table_tags 
                WHERE tag_name IN ('cls') 
               AND catalog_name = '{self.security_config.catalog}' 
               AND schema_name = '{self.security_config.schema}'"""
        ).collect()

    def _get_column_tags(self) -> List[Row]:
        """Retrieve column-level security tags."""
        logger.debug("Retrieving column-level security tags")
        return self.spark.sql(
            f"""SELECT * FROM {self.security_config.catalog}.information_schema.column_tags 
               WHERE tag_name IN ('cls') 
               AND catalog_name = '{self.security_config.catalog}' 
               AND schema_name = '{self.security_config.schema}'"""
        ).collect()

    def _get_functions(self) -> List[Row]:
        """Retrieve security functions from catalog."""
        logger.debug("Retrieving security functions")
        return self.spark.sql(
            f"""SELECT * FROM {self.security_config.catalog}.information_schema.routines 
               WHERE routine_type = 'FUNCTION' 
               AND specific_catalog = '{self.security_config.catalog}' 
               AND specific_schema = '{self.security_config.schema}'"""
        ).collect()

    def _validate_functions(
        self,
        df_tags_table: List[Row],
        df_tags_columns: List[Row],
        df_functions: List[Row],
    ) -> None:
        """Validate that all referenced functions exist."""
        function_names: Set[str] = {row["routine_name"] for row in df_functions}
        tag_function_names: Set[str] = {row["tag_value"] for row in df_tags_table}
        tag_function_names_columns: Set[str] = {
            row["tag_value"] for row in df_tags_columns
        }

        missing_functions = (
            tag_function_names | tag_function_names_columns
        ) - function_names
        if missing_functions:
            logger.error(f"Functions not found: {missing_functions}")
            raise ValueError(f"Functions not found: {missing_functions}")
        logger.info("All referenced functions validated successfully")

    def _parse_policies(
        self, df_tags_table: List[Row], df_tags_columns: List[Row]
    ) -> List[SecurityPolicy]:
        """Parse security policies from tags."""
        policies = []

        for row in df_tags_table:
            if row["tag_name"] == SecurityType.RLS.value:
                policies.append(
                    SecurityPolicy(
                        security_type=SecurityType.RLS,
                        table_name=row["table_name"],
                        function_name=row["tag_value"],
                    )
                )

        for row in df_tags_columns:
            if row["tag_name"] == SecurityType.CLS.value:
                policies.append(
                    SecurityPolicy(
                        security_type=SecurityType.CLS,
                        table_name=row["table_name"],
                        function_name=row["tag_value"],
                        column_name=row["column_name"],
                    )
                )

        logger.info(f"Parsed {len(policies)} security policies")
        return policies
    
    def _get_column_masks(self) -> List[Row]:
        """Retrieve existing column-level security masks."""
        logger.debug("Retrieving column-level security masks")
        return self.spark.sql(
            f"""SELECT * FROM {self.security_config.catalog}.information_schema.column_masks 
               WHERE table_catalog = '{self.security_config.catalog}' 
               AND table_schema = '{self.security_config.schema}'"""
        ).collect()
    
    def _validate_cls_policy(self, policy: SecurityPolicy, existing_masks: List[Row]) -> bool:
        """Check if column mask already exists for the policy."""
        full_function_name = f"{self.security_config.catalog}.{self.security_config.schema}.{policy.function_name}"
        for mask in existing_masks:
            if (mask["table_name"] == policy.table_name and 
                mask["column_name"] == policy.column_name and
                mask["mask_name"] == full_function_name):
                logger.warning(f"Column mask already exists for {policy.table_name}.{policy.column_name}")
                return False
        return True


    def _apply_rls_policy(self, policy: SecurityPolicy) -> None:
        """Apply row-level security policy."""
        full_table_name = f"{self.security_config.catalog}.{self.security_config.schema}.{policy.table_name}"
        full_function_name = f"{self.security_config.catalog}.{self.security_config.schema}.{policy.function_name}"

        logger.info(f"Applying RLS policy - Table: {full_table_name}, Function: {full_function_name}")
        self.spark.sql(
            f"ALTER TABLE {full_table_name} SET ROW FILTER {full_function_name}"
        )
        logger.info(f"Successfully applied RLS policy to {full_table_name}")

    def _apply_cls_policy(self, policy: SecurityPolicy) -> None:
        """Apply column-level security policy."""
        full_table_name = f"{self.security_config.catalog}.{self.security_config.schema}.{policy.table_name}"
        full_function_name = f"{self.security_config.catalog}.{self.security_config.schema}.{policy.function_name}"

        logger.info(f"Applying CLS policy - Table: {full_table_name}, Column: {policy.column_name}, Function: {full_function_name}")
        self.spark.sql(
            f"ALTER TABLE {full_table_name} ALTER COLUMN {policy.column_name} SET MASK {full_function_name}"
        )
        logger.info(f"Successfully applied CLS policy to {full_table_name}.{policy.column_name}")

    def apply_security_policies(self) -> List[Row]:
        """Main method to apply all security policies."""
        logger.info("Starting security policy application process")
        df_tags_table = self._get_table_tags()
        df_tags_columns = self._get_column_tags()
        df_functions = self._get_functions()
        existing_masks = self._get_column_masks()
        self._validate_functions(df_tags_table, df_tags_columns, df_functions) ### aby nie alteorować maski, które już istnieją. jezeli zmienia sie logika funkcji, zmien funkcje

        policies = self._parse_policies(df_tags_table, df_tags_columns)

        for policy in policies:
            if policy.security_type == SecurityType.RLS:
                self._apply_rls_policy(policy)
            elif policy.security_type == SecurityType.CLS:
                if self._validate_cls_policy(policy, existing_masks):
                    self._apply_cls_policy(policy)

        logger.info("Security policy application process completed successfully")
        return self._get_tables()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    config = get_config("qa")
    security_manager = DatabricksSecurityManager(config)
    tables = security_manager.apply_security_policies()
