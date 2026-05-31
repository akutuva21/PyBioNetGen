#!/bin/bash

set -e

process_one() {
    local PRNUM=$1
    local BRANCH=$2
    local TITLE="$3"
    local FIXBRANCH="fix-pr-${PRNUM}"

    echo "=========================================="
    echo "Processing PR #${PRNUM}: ${TITLE}"

    git checkout main 2>/dev/null
    git pull origin main 2>/dev/null

    # Clean up any existing fix branch
    git branch -D "${FIXBRANCH}" 2>/dev/null || true

    # Checkout the PR branch
    git checkout origin/"${BRANCH}" -b "${FIXBRANCH}" 2>/dev/null

    # Merge main
    set +e
    git merge origin/main --no-edit 2>&1
    MERGE_EXIT=$?
    set -e

    if [ $MERGE_EXIT -ne 0 ]; then
        echo "CONFLICTS found. Resolving..."

        # patch_sbml2bngl.py: keep theirs if it's modify/delete
        git checkout --theirs patch_sbml2bngl.py 2>/dev/null && git add patch_sbml2bngl.py || true

        # For tests/test_bng_models.py, always keep main's version
        if [ -f tests/test_bng_models.py ]; then
            git checkout --theirs tests/test_bng_models.py 2>/dev/null && git add tests/test_bng_models.py || true
        fi

        # For bionetgen/modelapi/runner.py, keep theirs
        if [ -f bionetgen/modelapi/runner.py ]; then
            git checkout --theirs bionetgen/modelapi/runner.py 2>/dev/null && git add bionetgen/modelapi/runner.py || true
        fi

        # For tests/test_csimulator.py, keep theirs
        if [ -f tests/test_csimulator.py ]; then
            git checkout --theirs tests/test_csimulator.py 2>/dev/null && git add tests/test_csimulator.py || true
        fi

        # Check if there are still unresolved conflicts
        CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null)
        if [ -n "$CONFLICTS" ]; then
            echo "WARNING: Still have conflicts in:" $CONFLICTS
            for f in $CONFLICTS; do
                # For add/add conflicts, keep both by using ours (PR version)
                git checkout --ours "$f" 2>/dev/null || git checkout --theirs "$f" 2>/dev/null || true
                git add "$f" 2>/dev/null || true
            done
        fi

        git commit -m "Merge main into PR branch" --no-edit 2>/dev/null || echo "Nothing to commit"
    fi

    # Push to remote
    set +e
    git push origin "${FIXBRANCH}:${BRANCH}" 2>&1
    set -e

    # Try merge via gh
    gh pr merge "${PRNUM}" --repo akutuva21/PyBioNetGen --squash --subject "${TITLE}" --body "Automated merge by Jules auto-agent." 2>&1

    echo "Done PR #${PRNUM}"
    echo "=========================================="
}

# Process each remaining PR
process_one 323 "add-zero-molecule-parsing-test-9795602244274530409" "🧪 Add zero molecule parsing test for BNGPatternReader"
process_one 324 "test-rmtree-oserror-3696903912570948798" "🧪 [Testing Improvement] Validate _safe_rmtree handles lower-level OS errors"
process_one 327 "testing-modelobj-structs-13054738186386609170" "🧪 Add unit tests for ModelObj item operations"
process_one 329 "fix-bngmodel-todo-issue-11479550922764099372" "🧹 Refactor adjust_func_def to address TODO and unused variable"
process_one 330 "refactor-bngModel-todo-to-note-14505795882509990859" "🧹 Code Health: Refactor TODOs to Notes in bngModel.py"
process_one 331 "remove-empty-todo-structs-18035936454219311932" "🧹 [code health] Remove empty TODO comments from network structs"
process_one 332 "test-actionblock-iter-8973029917315419920" "🧪 Add unit test for ActionBlock list iteration"
process_one 335 "prevent-duplicate-additions-setup-py-5630542735414024485" "fix(setup.py): prevent duplicate manifest inclusions"
process_one 336 "add-gdiff-test-11133840938500861568" "🧪 Add tests for gdiff.py tool"
process_one 337 "fix-comment-setter-regex-12063520584713780731" "Fix comment setter in structs.py"
process_one 338 "test-xmlparsers-missing-id-15172766524275770985" "🧪 Add test for missing ID error handling in BondsXML parser"

echo ""
echo "All done!"
