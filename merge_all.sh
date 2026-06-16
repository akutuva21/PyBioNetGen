#!/bin/bash
REPO="akutuva21/PyBioNetGen"
WORKDIR="C:\\Users\\Achyudhan\\OneDrive - University of Pittsburgh\\Desktop\\Achyudhan\\School\\PhD\\Research\\BioNetGen\\PyBioNetGen"

merge_pr() {
    local PR_NUM=$1
    local BRANCH=$2
    local TYPE=$3

    echo ""
    echo "=========================================="
    echo "Processing PR #$PR_NUM ($BRANCH) [$TYPE]"
    echo "=========================================="

    cd "$WORKDIR"

    git fetch origin main 2>&1 | tail -1
    git fetch origin "$BRANCH" 2>&1 | tail -1
    git checkout "$BRANCH" 2>&1 | tail -1

    set +e
    MERGE_OUT=$(git merge origin/main 2>&1)
    echo "$MERGE_OUT"

    if echo "$MERGE_OUT" | grep -q "CONFLICT"; then
        echo "Conflicts detected. Resolving..."
        # Get list of conflicted files
        CONFLICTED=$(git diff --name-only --diff-filter=U)
        echo "Conflicted files: $CONFLICTED"
        for cf in $CONFLICTED; do
            if [[ "$cf" == *.py && "$TYPE" == "fix" ]] && [[ "$cf" != tests/* ]]; then
                echo "Keeping PR changes for $cf"
                git checkout --ours -- "$cf"
            elif [[ "$cf" == *.py ]] || [[ "$cf" == tests/* ]]; then
                echo "Resolving $cf by keeping both sides"
                python resolve_conflicts.py "$cf"
            else
                echo "Keeping PR changes for $cf"
                git checkout --ours -- "$cf"
            fi
        done
        git add -A
        git commit -m "Merge main into branch, resolve conflicts"
    elif echo "$MERGE_OUT" | grep -q "Already up to date"; then
        echo "Already up to date, no merge needed"
    fi
    set -e

    git push origin "$BRANCH" 2>&1 | tail -1
    gh pr merge "$PR_NUM" --repo "$REPO" --squash
    echo "PR #$PR_NUM merged successfully"
}

merge_pr 527 "test-function-gen-string-14596172654307023112" "test"
merge_pr 528 "test-gen-string-moltype-7394950452375420266" "test"
merge_pr 529 "fix/remove-FIXME-double-bonds-12216291637563897193" "fix"
merge_pr 530 "test-rule-gen-string-6580954047996206196" "test"
merge_pr 531 "testing-improvement-repl-param-3756407388322308656" "test"
merge_pr 533 "test-gen-string-parameter-5218757950557121163" "test"
merge_pr 535 "testing-improvement-structs-comment-13863758712916026060" "test"
merge_pr 536 "raise-bngmodelerror-8033722994807130082" "fix"
merge_pr 537 "test-energypattern-genstring-17860189420800755178" "test"
merge_pr 538 "testing-improvement-structs-4147933409853088182" "test"
merge_pr 541 "testing-sympy-odes-repl-param-14393462678052208889" "test"
merge_pr 544 "testing-side-string-rule-5025066414790934300" "test"
merge_pr 545 "test-observable-gen-string-8174563756316453581" "test"

echo ""
echo "=========================================="
echo "ALL PRs PROCESSED"
echo "=========================================="
