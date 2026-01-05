aws configure - konfigurowanie polazenie poprzez key i access policy
aws ec2 create-key-pair --key-name tf_key_new --query 'KeyMaterial' --output text > tf_key_new.pem  - pobierania klucza 
To polecenie robi jedną bardzo konkretną rzecz:
tworzy nowy klucz SSH w AWS i zapisuje jego prywatną część do pliku na Twoim dysku. Rozłóżmy je na czynniki pierwsze, bez magii.


## jak sie dostac do vm :
 chmod 400 tf_key.pem
 ssh -i "tf_key.pem" ec2-3-145-197-108.us-east-2.compute.amazonaws.com