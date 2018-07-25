git filter-branch --commit-filter \
'if [ "$GIT_AUTHOR_NAME" = "Egor Egorov" ]; then \
export GIT_AUTHOR_NAME="egigoka";\
export GIT_AUTHOR_EMAIL=egigoka@gmail.com;\
export GIT_COMMITTER_NAME="egigoka";\
export GIT_COMMITTER_EMAIL=egigoka@gmail.com;\
fi;\
git commit-tree "$@"'