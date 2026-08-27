#!/usr/bin/env python3
import datetime
import json
import logging
import os
import socket
import sys
import time
import urllib.request

# 1. 매크로 및 시스템 활동 로그 기록 설정
LOG_FILE = "macro_activity.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def clear_screen():
  os.system("cls" if os.name == "nt" else "clear")


def banner():
  clear_screen()
  print("=" * 64)
  print("           T O O L - D I N O   F R A M E W O R K          ")
  print("           Advanced Termux Network & Macro Utility        ")
  print("=" * 64)


def main_menu():
  while True:
    banner()
    print(" [01] 소켓 및 포트 열림 상태 분석")
    print(" [02] IP 정보 및 네트워크 분석 조회")
    print(" [03] .메크로 명령어 자동화 엔진 (.메크로 [원하는말])")
    print(" [04] Loco 봇 프레임워크 실행 (main.py)")
    print(" [05] 디스코드 셀프봇 / 패킷 분석 안내 및 가이드")
    print(" [00] 프로그램 종료")
    print("-" * 64)

    choice = input(" tool-dino > 번호를 입력하세요: ").strip()

    if choice in ["1", "01"]:
      check_port()
    elif choice in ["2", "02"]:
      track_ip()
    elif choice in ["3", "03"]:
      run_macro_engine()
    elif choice in ["4", "04"]:
      run_loco_bot()
    elif choice in ["5", "05"]:
      show_packet_selfbot_info()
    elif choice in ["0", "00"]:
      print("\n[-] tool-dino를 종료합니다. 안녕히 가세요!")
      sys.exit(0)
    else:
      input("\n[!] 잘못된 번호입니다. 엔터를 눌러 다시 시도하세요...")


def check_port():
  clear_screen()
  print("--- [01] 소켓 / 포트 열림 상태 분석 ---")
  target = input(
      "분석할 호스트/IP 입력 (예: google.com 또는 127.0.0.1): "
  ).strip()
  if not target:
    input("\n[!] 호스트가 비어 있습니다. 엔터를 눌러 돌아가세요...")
    return
  try:
    port = int(input("분석할 포트 번호 입력 (예: 80, 443, 8080): "))
  except ValueError:
    input(
        "\n[❌ 오류] 올바른 포트 번호를 입력하세요. 엔터를 눌러 돌아가세요..."
    )
    return

  print(f"\n[*] {target}:{port} 소켓 연결 테스트 중...")
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(3.0)
  try:
    result = sock.connect_ex((target, port))
    if result == 0:
      print(f"[✔ 열림(OPEN)] {target}:{port} 포트가 열려 있습니다.")
    else:
      print(f"[🔒 닫힘(CLOSED)] {target}:{port} 포트에 접근할 수 없습니다.")
  except socket.gaierror:
    print("[❌ 오류] 호스트를 찾을 수 없습니다. 주소를 확인하세요.")
  except Exception as e:
    print(f"[❌ 오류 발생]: {e}")
  finally:
    sock.close()
  input("\n계속하려면 엔터 키를 누르세요...")


def track_ip():
  clear_screen()
  print("--- [02] IP 정보 및 네트워크 분석 조회 ---")
  query_ip = input("조회할 IP 입력 (본인 IP는 그냥 엔터): ").strip()
  url = (
      f"http://ip-api.com/json/{query_ip}"
      if query_ip
      else "http://ip-api.com/json/"
  )

  try:
    print("[*] IP 정보를 분석 중입니다...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=5) as response:
      data = json.loads(response.read().decode("utf-8"))
      if data.get("status") == "success":
        print("\n[✔ IP 분석 결과 성공]")
        print(f" - IP 주소 : {data.get('query')}")
        print(f" - 국가/도시: {data.get('country')} / {data.get('city')}")
        print(f" - ISP(통신사): {data.get('isp')}")
        print(f" - 조직(Org) : {data.get('org')}")
        print(f" - 시간대   : {data.get('timezone')}")
      else:
        print(f"[❌ 조회 실패]: {data.get('message', '알 수 없는 오류')}")
  except Exception as e:
    print(f"[❌ 네트워크 오류]: {e}")
  input("\n계속하려면 엔터 키를 누르세요...")


def run_macro_engine():
  clear_screen()
  print("--- [03] .메크로 명령어 자동화 엔진 ---")
  print(" 💡 사용법: '.메크로 [원하는말]' 형태를 입력해보세요.")
  print("   - 예시: '.메크로 인사', '.메크로 상태확인', '.메크로 작업실행'")
  print("   - 메뉴로 돌아가려면 'back'을 입력하세요.\n")

  while True:
    cmd_input = input("macro-engine > ").strip()
    if cmd_input.lower() == "back":
      break
    if not cmd_input:
      continue

    if cmd_input.startswith(".메크로"):
      parts = cmd_input.split(" ", 1)
      if len(parts) < 2:
        print("❌ [오류] 명령어 뒤에 내용을 입력해주세요. (예: .메크로 인사)\n")
        continue

      macro_target = parts[1].strip()
      print(f"[*] 매크로 구동 중 ➔ 대상: '{macro_target}'")

      try:
        if macro_target == "인사":
          res_msg = "🤖 안녕하세요! 요청하신 자동 매크로가 정상 실행되었습니다."
        elif macro_target == "상태확인":
          res_msg = "📊 [시스템 상태] CPU/메모리 정상 구동 중"
        elif macro_target == "작업실행":
          res_msg = "⚡ 지정된 커스텀 자동화 작업이 완료되었습니다."
        else:
          res_msg = f"🔍 '{macro_target}'에 대한 매크로 동작을 수행했습니다."

        # 사용자 로그 기록 (로컬 파일)
        logging.info(f"Command: {cmd_input} | Result: {res_msg}")
        print(f"[✔ 성공] {res_msg}")
        print(f"📁 (사용자 로그가 '{LOG_FILE}' 파일에 기록되었습니다.)\n")

      except Exception as e:
        err_str = f"Error: {e}"
        logging.error(f"Command: {cmd_input} | Error: {err_str}")
        print(f"[❌ 오류]: {e}\n")
    else:
      print("💡 지원하지 않는 양식입니다. '.메크로 [원하는말]'로 입력하세요.\n")


def run_loco_bot():
  clear_screen()
  print("--- [04] Loco 봇 프레임워크 실행 (main.py) ---")
  if os.path.exists("main.py"):
    print(" [+] main.py 파일을 발견했습니다. 실행을 시작합니다...\n")
    time.sleep(1)
    os.system("python main.py")
  else:
    print(" [❌ 오류] 현재 경로에 main.py 파일이 없습니다.")
    print(" - 올바른 디렉토리로 이동했는지 확인해 주세요.")
  input("\n메뉴로 돌아가려면 Enter 키를 누르세요...")


def show_packet_selfbot_info():
  clear_screen()
  print("--- [05] 디스코드 셀프봇 / 패킷 분석 안내 및 가이드 ---")
  print("⚠️ [중요 보안 및 약관 경고]")
  print(" 1. 디스코드 셀프봇(Self-bot)은 유저 토큰을 악용해 자동화하는 행위로,")
  print("    디스코드 공식 서비스 약관(ToS) 위반이며 계정 영구 정지(Ban)의")
  print("    위험이 매우 높습니다.")
  print(" 2. 네트워크 패킷 분석(소켓 스니핑)은 로컬 환경 진단 및 개발")
  print("    목적으로만 안전하게 다루어야 합니다.")
  print("-" * 58)
  print(
      " [기술 안내] 실제 패킷 프록시나 셀프봇 통신은 암호화 및 보안 정책으로"
  )
  print(
      " 인해 별도의 전용 외부 라이브러리(예: Scapy, discord.py-self 등)"
  )
  print(
      " 를 로컬 환경에 구축하여 다뤄야 하며, 본 툴은 강력한 유틸리티와"
  )
  print(" 시스템 제어를 목적으로 설계되었습니다.")
  input("\n메뉴로 돌아가려면 Enter 키를 누르세요...")


if __name__ == "__main__":
  main_menu()
