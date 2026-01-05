## cut commits history: 
git branch --unset-upstream

vim CONTRIBUTING.md - zawartosc plików


git status -s - status plików w skróconej wersjin

git status vs git diff: git diff shows you the
exact lines added and removed

git diff --staged
git diff --cached to see what you’ve staged so far (--staged and --cached are synonyms



commits: 

git commit -a - nie trzeba git add dawac to stage - ale tylko zmiany plikow, dodanie plikow i tak trzba git add
git commit --amend - zmienia ostatni commit
git commit --amend -m "New commit message" - zmienia ostatni commit z nowa wiadomoscia
git reset HEAD~1 - cofa ostatni commit, ale zostawia zmiany w plikach
git reset --soft HEAD~1 - cofa ostatni commit, ale zostawia zmiany w stage
git reset --hard HEAD~1 - cofa ostatni commit i usuwa zmiany w plikach
git commit -am "message" - dodaje wszystkie zmiany i robi commit z wiadomoscia
git commit --amend: pozwala zmienić ostatni commit (np. dodać zapomniane pliki lub zmienić wiadomość)
Git mówi:
„Zastąp ostatni commit nowym, poprawionym snapshotem.”
To nie jest „nowy commit + poprawka”.
To jest podmiana ostatniego commita.
Typowy scenariusz (dokładnie ten z opisu)
Robisz commit
Po 10 sekundach orientujesz się:
zapomniałeś pliku
zapomniałeś zmiany
message jest słaby
Robisz poprawki
Dodajesz je do staging

git commit --amend --no-edit  - Poprawa bez zmiany message





removing: 
git rm --cached README.md - usuwa plik z repozytorium, ale zostawia go na dysku
git rm -r --cached . - usuwa wszystkie pliki z repozytorium, ale zostawia je na dysku
git rm -f file.txt - usuwa plik z repozytorium i z dysku
git rm \*~


moving files: 
Unlike many other VCSs, Git doesn’t explicitly track file movement
git mv file_from file_to - also renaming it




Logi: 

git log lists the commits
One of the more helpful options is -p or --patch, which shows the difference (the patch output)
introduced in each commit.
git log --pretty=oneline - shows each commit on a single line
git log --stat - shows stats of changes in each commit
git log --graph - shows a graph of the commit history
git log --pretty=format:"%h - %an, %ar : %s" - custom format
git log --since=2.weeks
git log -S function_name



Unstaging a Staged File: 
git reset HEAD CONTRIBUTING.md
It’s true that git reset can be a dangerous command, especially if you provide the
--hard flag.

Unmodifying a Modified File

$ git checkout -- CONTRIBUTING.md  wowczas przywraca plik do ostatniego commita, usunie wszystkie zmiany w pliku
It’s important to understand that git checkout -- <file> is a dangerous command.
Any local changes you made to that file are gone — Git just replaced that file with
the last staged or committed version. Remember, anything that is committed in Git can almost always be recovered. Even commits that
were on branches that were deleted or commits that were overwritten with an --amend commit can
be recovered


git restore
git restore. It’s basically an alternative to git reset HEAD <file> for unstaging files and git checkout -- <file> for discarding changes in
git restore --staged CONTRIBUTING.md


remote: 
git remote add origin <url>
git push -u origin main
git push origin --delete <branch_name> - usuwa zdalna galezn
git fetch origin
git pull origin main
git clone <url>
git remote -v - shows remote repositories
git remote show origin - shows detailed info about remote repository
git remote rename origin new_name - renames remote repository
git remote remove new_name - removes remote repository
git remote add :NIC nie tworzy na GitHubie.
Nie zakłada repozytorium, nie wysyła kodu, nie kontaktuje się z serwerem.
    Masz repo w dwóch miejscach (backup/migracja)
    git remote add backup git@gitlab.com:lukasz/codes.git
    git push backup main

git fetch <remote>
 - pulls down all the data from that remote project
that you don’t have yet. After you do this, you should have references to all the branches from that
remote, which you can merge in or inspect at any time.
git pull <remote> <branch>
 - does a git fetch followed by a git merge
git fetch

Pobierz cudzą historię. Niczego nie ruszaj u mnie.

git pull

Pobierz cudzą historię i NATYCHMIAST spróbuj ją połączyć z moją.

git pull = git fetch + git merge
git fetch origin

Tak — ściąga wszystkie branche z repozytorium origin, których:

jeszcze nie masz

albo które się zmieniły
Co się NIE dzieje przy fetch

Po git fetch:

❌ nie zmienia się HEAD

❌ nie zmienia się aktualny branch

❌ nie ma merge’a

❌ nie ma konfliktów

Co robi git pull origin main

Zakładając, że jesteś na branchu main:

git pull origin main


Kroki:

git fetch origin

git merge origin/main → od razu

Czyli:

lokalny main się zmienia

mogą pojawić się konflikty

historia może zostać zmodyfikowana

pull to skrót dla niecierpliwych albo pewnych sytuacji.

git fetch origin
git log main..origin/main
git merge origin/main

Dlatego doświadczeni devowie często:

git fetch
git diff main..origin/main


i dopiero potem decydują.

Co oznacza git diff main..origin/main

Czytaj to tak:

„Pokaż mi różnice między moim lokalnym main
a tym, jak main wygląda na serwerze (origin).”

Czyli:

lewa strona (main) → Twój lokalny branch

prawa strona (origin/main) → migawka brancha main na GitHubie, pobrana przez git fetch

git fetch command only downloads
the data to your local repository — it doesn’t automatically merge it with any of your work or
modify what you’re currently working on. You have to merge it manually into your work when
you’re ready.


Running git pull generally fetches data from the server you originally cloned from and
automatically tries to merge it into the code you’re currently working on.

Git pull: 

Fast-forward nic nie tworzy.
Merge tworzy nowy commit.
Rebase przepisuje stare.

A---B---C   main (u Ciebie)
A---B---C---D   origin/main

Fast-forward. Fast-forward = „przesuń wskaźnik do przodu”
Nie powstaje żaden nowy commit.
Co robi Git
Twój main jest dokładnie w tyle za origin/main. Efekt:
A---B---C---D   main, origin/main

Commit merge
Ty zrobiłeś commit E lokalnie:

A---B---C---E   main

Na serwerze ktoś zrobił D:

A---B---C---D   origin/main
Historie się rozgałęziły.
Git tworzy NOWY commit, który „łączy” obie historie.
A---B---C---E---M   main
         \     /
          D---
mówi: „od tego miejsca obie linie są połączone”

Rebase (przepisanie historii)

Ten sam punkt startowy:

A---B---C---E   main
A---B---C---D   origin/main

Co robi rebase

Git mówi:

„Weź mój commit E, oderwij go i przyklej na koniec origin/main”.

Efekt:

A---B---C---D---E'   main


git push <remote> <branch>. 
If you want to push your master branch to
your origin server (again, cloning generally sets up both of those names for you automatically),
then you can run this to push any commits you’ve done back up to the server:
$ git push origin master


Inspecting a Remote

git remote show
<remote> command. For example, to see detailed information about the origin remote, you can run:
$ git remote show origin
git remote show origin
It shows you the URL of the remote repository, the fetch and push branches, and other
information about the remote repository.

git remote show <remote> shows detailed information about the specified remote repository, including its URL, fetch and push branches, and other relevant details.

$ git remote rename pb paul
$ git remote
It’s worth mentioning that this changes all your remote-tracking branch names, too. What used to
be referenced at pb/master is now at paul/master.

usuwanie tego zdalnego repozytorium: 
$ git remote remove paul
$ git remote

tags: 
git tag v1.0 - tworzy tag v1.0 na ostatnim commicie
git tag -a v1.0 -m "version 1.0" - tworzy tag v1.0 z opisem
git tag -l - pokazuje wszystkie tagi
git show v1.0 - pokazuje informacje o tagu v1.0
Git supports two types of tags: lightweight and annotated.
A lightweight tag is very much like a branch that doesn’t change — it’s just a pointer to a specific
commit.
Annotated tags, however, are stored as full objects in the Git database. They’re checksummed;
contain the tagger name, email, and date; have a tagging message; and can be signed and verified
with GNU Privacy Guard (GPG). It’s generally recommended that you create annotated tags so you
can have all this information; but if you want a temporary tag or for some reason don’t want to
keep the other information, lightweight tags are available too.
To create an annotated tag, use the -a option when creating the tag:
$ git tag -a v1.4 -m "my version 1.4"
This creates a tag named v1.4 with the message “my version 1.4”.
To see the details of an annotated tag, you can use the git show command:

$ git show v1.4

git show v1.4-lw

Tagging Later
You can also tag commits after you’ve moved past them. Suppose your commit history looks like
this:

By default, the git push command doesn’t transfer tags to remote servers. You will have to explicitly
push tags to a shared server after you have created them


# lista
git tag
git tag -l "v1.*"

# annotated tag dla release
git tag -a v1.0.0 -m "Release v1.0.0"

# tag na konkretny commit
git tag -a v1.0.0 <sha> -m "Release v1.0.0"

# wysłanie taga
git push origin v1.0.0
git push origin --tags
git push origin --follow-tags

# usunięcie taga
git tag -d v1.0.0
git push origin --delete v1.0.0
