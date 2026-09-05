# GitHub 업로드 방법

## 1. GitHub에서 빈 저장소 만들기

1. GitHub에 로그인합니다.
2. 오른쪽 위 `+` 버튼을 누릅니다.
3. `New repository`를 선택합니다.
4. 저장소 이름을 `rune-timer` 또는 `rune-timer-alert`로 입력합니다.
5. `Public`을 선택합니다.
6. `Add a README file`, `.gitignore`, `license`는 체크하지 않습니다.
7. `Create repository`를 누릅니다.

## 2. 로컬 저장소 연결하기

GitHub에서 저장소를 만든 뒤, 아래 명령에서 `YOUR_ID` 부분만 본인 GitHub 아이디로 바꿔서 실행합니다.

```powershell
cd "$env:USERPROFILE\Desktop\rune-timer-github"
git remote add origin https://github.com/YOUR_ID/rune-timer.git
git push -u origin main
```

## 3. 이미 origin이 있다고 뜨는 경우

```powershell
git remote set-url origin https://github.com/YOUR_ID/rune-timer.git
git push -u origin main
```

## 4. GitHub 로그인 창이 뜨는 경우

브라우저 또는 Git Credential Manager 로그인 창이 뜨면 GitHub 계정으로 로그인하면 됩니다.
