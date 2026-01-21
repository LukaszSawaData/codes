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

# usunięcie taga
git tag -d v1.0.0
git push origin --delete v1.0.0

$ git checkout v2.0.0
Note: switching to 'v2.0.0'.
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.
If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:
git switch -c <new-branch-name>
Or undo this operation with:
git switch -
Turn off this advice by setting config variable advice.detachedHead to false
HEAD is now at 99ada87... Merge pull request #89 from schacon/appendix-final
$ git checkout v2.0-beta-0.1
Previous HEAD position was 99ada87... Merge pull request #89 from schacon/appendixfinal
HEAD is now at df3f601... Add atlas.json and cover image

Aliases
$ git config --global alias.co checkout
$ git config --global alias.br branch
$ git config --global alias.ci commit
$ git config --global alias.st status
This means that, for example, instead of typing git commit, you just need to type git ci. As you go
on using Git, you can add more aliases for commands you use often.
git config --global alias.unstage 'reset HEAD --' 
$ git config --global alias.last 'log -1 HEAD'

branching:
git branch new_feature - tworzy nową gałąź new_feature
git checkout new_feature - przełącza na gałąź new_feature
git checkout -b new_feature - tworzy i przełącza na gałąź new_feature
git branch -d new_feature - usuwa gałąź new_feature
git branch -D new_feature - wymusza usunięcie gałęzi new_feature
git merge new_feature - łączy gałąź new_feature z aktualną gałęzią
git rebase main - przepisuje historię aktualnej gałęzi na bazie main
git branch -a - pokazuje wszystkie gałęzie, w tym zdalne
git branch -vv - pokazuje wszystkie gałęzie z informacją o ostatnim commicie
git checkout - - przełącza na poprzednią gałąź
git switch new_feature - przełącza na gałąź new_feature (nowa składnia          
git switch -c new_feature - tworzy i przełącza na gałąź new_feature (nowa składnia          
git switch - - przełącza na poprzednią gałąź (nowa składnia     

When you make a commit, Git stores a commit object that contains a pointer to the snapshot of the
content you staged. This object also contains the author’s name and email address, the message that
you typed, and pointers to the commit or commits that directly came before this commit (its parent
or parents): zero parents for the initial commit, one parent for a normal commit, and multiple
parents for a commit that results from a merge of two or more branches.


To visualize this, let’s assume that you have a directory containing three files, and you stage them
all and commit. Staging the files computes a checksum for each one (the SHA-1 hash we mentioned
in What is Git?), stores that version of the file in the Git repository (Git refers to them as blobs), and
adds that checksum to the staging area:

A branch in Git is simply a lightweight movable pointer to one of these commits. The default branch
name in Git is master. As you start making commits, you’re given a master branch that points to the
last commit you made. Every time you commit, the master branch pointer moves forward
automatically.

How does Git know what branch you’re currently on? It keeps a special pointer called HEAD. Note
that this is a lot different than the concept of HEAD in other VCSs you may be used to, such as
Subversion or CVS. In Git, this is a pointer to the local branch you’re currently on. In this case,
you’re still on master. The git branch command only created a new branch — it didn’t switch to that
65
branch.

sprawdzenie heade: git log --oneline --decorate

git checkout testing
This moves HEAD to point to the testing branch.

When you create a new branch, what you’re really doing is creating a new pointer to the current
commit. So, if you create a new branch called testing while you’re on master, both branches point to
the same commit. When you switch to the testing branch, HEAD now points to testing instead of
master. When you make a new commit, the testing branch pointer moves forward automatically
to point to the new commit, while master stays where it is.

git log --oneline --decorate
--graph --all

Creating a new branch and switching to it at the same time
It’s typical to create a new branch and want to switch to that new branch at the
same time — this can be done in one operation with git checkout -b
<newbranchname>.

From Git version 2.23 onwards you can use git switch instead of git checkout to:
• Switch to an existing branch: git switch testing-branch.
• Create a new branch and switch to it: git switch -c new-branch. The -c flag
stands for create, you can also use the full flag: --create.
• Return to your previously checked out branch: git switch -.

$ git checkout -b iss53
Switched to a new branch "iss53"
This is shorthand for:
$ git branch iss53
$ git checkout iss53



checkouting: 
However, before you do that, note that if your working directory or staging area has uncommitted
changes that conflict with the branch you’re checking out, Git won’t let you switch branches. It’s
best to have a clean working state when you switch branches. There are ways to get around this
(namely, stashing and commit amending) that we’ll cover later on, in Stashing and Cleaning. For
now, let’s assume you’ve committed all your changes, so you can switch back to your master branch:

At this point, your project working directory is exactly the way it was before you started working
on issue #53, and you can concentrate on your hotfix. This is an important point to remember:
when you switch branches, Git resets your working directory to look like it did the last time you
committed on that branch. It adds, removes, and modifies files automatically to make sure your
working copy is what the branch looked like on your last commit to it.


git checkout -b feature2 HEAD~1
To jest jedno polecenie, które robi dwie rzeczy naraz.
HEAD = branch, na którym merge’ujesz



git rm -r --cached .terraform
echo ".terraform/" >> .gitignore
git add .gitignore
git commit -m "Remove terraform provider cache from git"
git push -u origin test_feat


git rebase main
git reset main
git push -u origin test_feat --force
git pull origin main
git push -u origin main




git rebase main
git reset main
git push -u origin test_feat --force
git pull origin main
git push -u origin main

