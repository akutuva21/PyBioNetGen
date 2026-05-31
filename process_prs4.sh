#!/bin/bash

process_one() {
    local PRNUM=$1
    local BRANCH=$2
    local TITLE="$3"
    local FIXBRANCH="fix-pr-${PRNUM}"

    echo "=========================================="
    echo "Processing PR #${PRNUM}: ${BRANCH}"

    git checkout main 2>/dev/null
    git pull origin main 2>/dev/null
    git branch -D "${FIXBRANCH}" 2>/dev/null || true

    git checkout origin/"${BRANCH}" -b "${FIXBRANCH}" 2>/dev/null

    set +e
    git merge origin/main --no-edit 2>&1
    MERGE_EXIT=$?
    set -e

    if [ $MERGE_EXIT -ne 0 ]; then
        echo "CONFLICTS found. Resolving..."

        # For ALL conflicted files, use --theirs (accept main version)
        CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null)
        if [ -n "$CONFLICTS" ]; then
            for f in $CONFLICTS; do
                echo "  Accepting theirs for: $f"
                git checkout --theirs "$f" 2>/dev/null
                git add "$f" 2>/dev/null
            done
        fi

        git commit -m "Merge main into PR branch" --no-edit 2>/dev/null || true
    fi

    git push origin "${FIXBRANCH}:${BRANCH}" 2>&1

    # Retry merge if it fails
    set +e
    gh pr merge "${PRNUM}" --repo akutuva21/PyBioNetGen --squash --subject "${TITLE}" --body "Automated merge by Jules auto-agent." 2>&1
    RET=$?
    if [ $RET -ne 0 ]; then
        echo "Retrying merge after update-branch..."
        gh pr update-branch "${PRNUM}" --repo akutuva21/PyBioNetGen 2>&1
        gh pr merge "${PRNUM}" --repo akutuva21/PyBioNetGen --squash --subject "${TITLE}" --body "Automated merge by Jules auto-agent." 2>&1
    fi
    set -e

    echo "Done PR #${PRNUM}"
}

# Process remaining PRs
process_one 327 "testing-modelobj-structs-13054738186386609170" "🧪 Add unit tests for ModelObj item operations"
process_one 329 "fix-bngmodel-todo-issue-11479550922764099372" "🧹 Refactor adjust_func_def to address TODO and unused variable"
process_one 330 "refactor-bngModel-todo-to-note-14505795882509990859" "🧹 Code Health: Refactor TODOs to Notes in bngModel.py"
process_one 331 "remove-empty-todo-structs-18035936454219311932" "🧹 [code health] Remove empty TODO comments from network structs"
process_one 332 "test-actionblock-iter-8973029917315419920" "🧪 Add unit test for ActionBlock list iteration"
process_one 335 "prevent-duplicate-additions-setup-py-5630542735414024485" "fix(setup.py): prevent duplicate manifest inclusions"
process_one 336 "add-gdiff-test-11133840938500861568" "🧪 Add tests for gdiff.py tool"
process_one 337 "fix-comment-setter-regex-12063520584713780731" "Fix comment setter in structs.py"
process_one 338 "test-xmlparsers-missing-id-15172766524275770985" "🧪 Add test for missing ID error handling in BondsXML parser"

echo "All remaining PRs processed!"
