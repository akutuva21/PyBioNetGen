param(
  [string]$Repo = "akutuva21/PyBioNetGen",
  [int]$Start = 0,
  [int]$End = 9999,
  [string]$PythonExe = "C:/Users/Achyudhan/anaconda3/envs/Research/python.exe"
)

$prs = gh pr list -R $Repo --state open --limit 200 --json number | ConvertFrom-Json | Sort-Object number
$results = @()

foreach ($p in $prs) {
  $num = [int]$p.number
  if ($num -lt $Start -or $num -gt $End) { continue }

  try {
    $prMeta = gh pr view $num -R $Repo --json headRefName,files | ConvertFrom-Json
    $branch = $prMeta.headRefName
  } catch {
    $results += [pscustomobject]@{ PR = $num; Branch = "?"; Status = "meta-failed"; Details = $_.Exception.Message }
    continue
  }

  try { git checkout main | Out-Null } catch {}
  try {
    gh pr checkout $num -R $Repo | Out-Null
  } catch {
    $results += [pscustomobject]@{ PR = $num; Branch = $branch; Status = "checkout-failed"; Details = $_.Exception.Message }
    continue
  }

  if (Test-Path ".jules") {
    git rm -r --cached --ignore-unmatch .jules | Out-Null
    Remove-Item -Recurse -Force .jules
  }

  if (-not (Test-Path ".gitignore")) {
    New-Item -ItemType File -Path .gitignore | Out-Null
  }

  $gi = @()
  if (Test-Path ".gitignore") {
    $gi = Get-Content .gitignore
  }
  if (-not ($gi -contains ".jules/")) {
    Add-Content .gitignore ".jules/"
  }
  if (-not ($gi -contains "__pycache__/")) {
    Add-Content .gitignore "__pycache__/"
  }

  $pyFiles = @(
    $prMeta.files |
      ForEach-Object { $_.path } |
      Where-Object { $_ -match "\\.py$" -and (Test-Path $_) } |
      Sort-Object -Unique
  )

  foreach ($f in $pyFiles) {
    & $PythonExe -m black --quiet $f
  }

  if (git status --porcelain) {
    git add -A
    git commit -m "chore: PR #$num remove forbidden artifacts and run black" | Out-Null
    try {
      git push origin HEAD:$branch | Out-Null
      $results += [pscustomobject]@{ PR = $num; Branch = $branch; Status = "pushed-fixes"; Details = "cleanup+black" }
    } catch {
      try {
        git pull --rebase origin $branch | Out-Null
        git push origin HEAD:$branch | Out-Null
        $results += [pscustomobject]@{ PR = $num; Branch = $branch; Status = "pushed-after-rebase"; Details = "cleanup+black" }
      } catch {
        $results += [pscustomobject]@{ PR = $num; Branch = $branch; Status = "push-failed"; Details = $_.Exception.Message }
      }
    }
  } else {
    $results += [pscustomobject]@{ PR = $num; Branch = $branch; Status = "no-changes"; Details = "already clean" }
  }
}

git checkout main | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$out = "tmp_pr_remediation_${Start}_${End}_${stamp}.csv"
$results | Sort-Object PR | Export-Csv -Path $out -NoTypeInformation
Write-Output "WROTE $out"
$results | Group-Object Status | Sort-Object Count -Descending | Format-Table Count, Name -AutoSize
