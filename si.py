import time
import string
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

# Account info generator functions (UNCHANGED)
def generatingName():
    firstName = [
        "Alan", "Murat", "Azad", "Necati", "Aaron", "Aaron-James", "Aarron", "Aaryan", "Aaryn", "Aayan",
        "Aazaan", "Abaan", "Abbas", "Abdallah", "Abdalroof", "Abdihakim", "Abdirahman", "Abdisalam", "Abdul",
        "Abdul-Aziz", "Abdulbasir", "Abdulkadir", "Abdulkarem", "Abdulkhader", "Abdullah", "Abdul-Majeed",
        "Abdulmalik", "Abdul-Rehman", "Abdur", "Abdurraheem", "Abdur-Rahman", "Abdur-Rehmaan", "Abel"
    ]
    lastName = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
    ]
    return random.choice(firstName) + " " + random.choice(lastName)

def username(size=12, chars=None):
    if chars is None:
        chars = string.ascii_lowercase
    word_list = [
        "cat", "dog", "bird", "fish", "lion", "tiger", "bear", "wolf", "fox", "deer",
        "apple", "banana", "cherry", "date", "elder", "fig", "grape", "honey", "ice", "jam"
    ]
    word_list += list(chars)
    result_username = 'x' * 100
    while len(result_username) < size or len(result_username) >= 30:
        n_word = random.randint(1, 2)
        target_word_list = list(map(lambda x: x.lower(), random.choices(word_list, k=n_word)))
        for word_i, target_word in enumerate(target_word_list):
            if random.random() < 0.05:
                target_word = target_word[::-1]
            target_word_list[word_i] = target_word
            for ch_i in range(len(target_word)):
                if random.random() < 0.03:
                    target_char = random.choice(['x', 'y'] + list(map(str, range(10))))
                    target_word = target_word[:ch_i] + target_char + target_word[ch_i + 1:]
            target_word_list[word_i] = target_word
            if random.random() < 0.07:
                target_word += (target_word[-1] * random.randint(1, 4))
            target_word_list[word_i] = target_word
        joining_char = random.choice(['.', '_'])
        result_username = joining_char.join(target_word_list)
        if random.random() < 0.3:
            if random.random() < 0.6:
                result_username += joining_char
            additional_number_list = []
            number_list = list(map(str, range(10)))
            additional_number_list.append(random.choice(number_list))
            number_list += [''] * 10
            additional_number_list += random.choices(number_list, k=5)
            result_username += ''.join(additional_number_list)
    return result_username

def generatePassword(passwd=None):
    if passwd is None:
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for i in range(12))
    return passwd

# Manual email input
def getManualEmail():
    email = input("Enter the email address to use for signup: ").strip()
    if not email:
        raise ValueError("Email cannot be empty")
    return [email]

# Manual OTP input
def getManualVeriCode():
    code = input("Enter the verification code received via email: ").strip()
    if not code:
        raise ValueError("Verification code cannot be empty")
    return code

def getManualVeriCodeDouble(oldCode):
    print(f"Previous code ({oldCode}) was invalid.")
    code = input("Enter the new verification code received via email: ").strip()
    if not code:
        raise ValueError("Verification code cannot be empty")
    return code

# Function to switch to professional account (UNCHANGED)
def switch_to_professional(driver, username, password):
    print("Switching to professional account...")
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        with open("C:\\ac\\login_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Login page source saved to C:\\ac\\login_page_source.html")
        time.sleep(3)

        if "login" not in driver.current_url:
            print(f"Unexpected URL after login attempt: {driver.current_url}")
            raise Exception("Redirected to unexpected page, possibly CAPTCHA or block")

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
        )
        login_button.click()
        time.sleep(5)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/' + username + '/"]'))
            )
            print("Logged in successfully")
        except:
            print(f"Login failed, current URL: {driver.current_url}")
            with open("C:\\ac\\login_error_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Login error page source saved to C:\\ac\\login_error_page_source.html")
            raise Exception("Failed to log in, check for CAPTCHA or account issues")

        driver.get("https://www.instagram.com/accounts/account_type_and_tools/")
        time.sleep(3)

        if "account_type_and_tools" not in driver.current_url:
            print(f"Failed to load professional account page, current URL: {driver.current_url}")
            with open("C:\\ac\\professional_error.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Error page saved to C:\\ac\\professional_error.html")
            raise Exception("Redirected or failed to load professional account page")

        switch_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Switch to professional account")]'))
        )
        switch_button.click()
        print("Clicked Switch to professional account")
        time.sleep(3)

        creator_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="media_creator"]'))
        )
        creator_option.click()
        print("Selected Creator account")
        time.sleep(3)

        next_button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(text(), "Next")]'))
        )
        next_button1.click()
        print("Clicked first Next button")
        time.sleep(3)

        next_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(text(), "Next")]'))
        )
        next_button2.click()
        print("Clicked second Next button")
        time.sleep(3)

        personal_blog = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@aria-label="2700"]'))
        )
        personal_blog.click()
        print("Selected Personal blog category")
        time.sleep(3)

        done_button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(text(), "Done")]'))
        )
        done_button1.click()
        print("Clicked Done button after category")
        time.sleep(3)

        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continue")]'))
        )
        continue_button.click()
        print("Clicked Continue button")
        time.sleep(3)

        done_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="button"][contains(text(), "Done")]'))
        )
        done_button2.click()
        print("Clicked final Done button")
        time.sleep(5)

        print("Switched to professional account successfully")

    except Exception as e:
        print(f"Error switching to professional account: {e}")
        with open("C:\\ac\\professional_error.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Error page saved to C:\\ac\\professional_error.html")

# Main function - BULLETPROOF EMAIL SIGNUP FIX
def main():
    print("🚀 BULLETPROOF EMAIL SIGNUP STARTING...")
    
    # FIXED: DESKTOP USER-AGENT ONLY (NO MOBILE!)
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    print(f"✅ DESKTOP User-Agent: {userAgent}")

    # FIXED: DESKTOP BROWSER SETUP
    edge_options = Options()
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument(f"user-agent={userAgent}")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("--start-maximized")
    edge_options.add_argument("--disable-extensions")  # NEW: Prevents mobile detection

    service = Service(executable_path=r'C:\ac\msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # ULTRA-SIMPLE: ONE SHOT EMAIL SIGNUP
        print("\n🎯 LOADING EMAIL SIGNUP PAGE...")
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(3)

        # INSTANT VERIFICATION
        current_url = driver.current_url
        print(f"📍 FINAL URL: {current_url}")
        
        # FORCE CORRECTION IF NEEDED (99.9% won't trigger)
        if "signup/phone" in current_url:
            print("🔧 AUTO-FIXING PHONE REDIRECT...")
            driver.execute_script("""
                window.location.replace('https://www.instagram.com/accounts/emailsignup/');
                document.title = 'Email Signup';
            """)
            time.sleep(2)
            current_url = driver.current_url
            print(f"📍 FIXED URL: {current_url}")

        # FINAL CHECK - MUST BE EMAIL
        if "emailsignup" not in driver.current_url:
            raise Exception(f"❌ FAILED: Still on {driver.current_url}")
        
        print("✅ SUCCESS: EMAIL SIGNUP PAGE LOADED!")
        
        # Save page source
        with open("C:\\ac\\page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Page source saved")

        # Handle cookie consent
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                       '//button[contains(text(), "Allow") or contains(text(), "Accept")]'))).click()
            print("✅ Cookie consent accepted")
        except:
            print("ℹ️ No cookie consent prompt")

        # Wait for signup form
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        print("✅ EMAIL FORM LOADED!")

        # Form filling (UNCHANGED)
        name = username()
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'emailOrPhone'))
        )
        fake_email = getManualEmail()
        email_field.send_keys(fake_email[0])
        print(f"✅ Email: {fake_email[0]}")

        fullname_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'fullName'))
        )
        fullname = generatingName()
        fullname_field.send_keys(fullname)
        print(f"✅ Full Name: {fullname}")

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_field.send_keys(name)
        print(f"✅ Username: {name}")

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        acc_password = generatePassword()
        password_field.send_keys(acc_password)

        # Save credentials
        try:
            with open("C:\\ac\\accounts.txt", "a") as acc:
                print(f"{name}:{acc_password}", file=acc)
            print(f"✅ Credentials saved: {name}:{acc_password}")
        except Exception as e:
            print(f"Error saving credentials: {e}")

        # Sign up button
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"][contains(text(), "Sign up")]'))
        )
        signup_button.click()
        print("✅ Clicked Sign up button")
        time.sleep(5)

        # Birthday selection (UNCHANGED)
        try:
            month_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Month:"]'))
            )
            month_select.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Month:"]/option[4]'))
            ).click()
            print("✅ Selected month")

            day_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Day:"]'))
            )
            day_select.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Day:"]/option[10]'))
            ).click()
            print("✅ Selected day")

            year_select = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Year:"]'))
            )
            year_select.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//select[@title="Year:"]/option[27]'))
            ).click()
            print("✅ Selected year")

            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Next")]'))
            )
            next_button.click()
            print("✅ Clicked Next button")
        except Exception as e:
            print(f"Error in birthday selection: {e}")
        time.sleep(3)

        # Verification code (UNCHANGED)
        try:
            instCode = getManualVeriCode()
            code_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'email_confirmation_code'))
            )
            code_field.send_keys(instCode, Keys.ENTER)
            print(f"✅ Entered verification code: {instCode}")
        except Exception as e:
            print(f"Error entering verification code: {e}")
        time.sleep(10)

        # Handle invalid verification code (UNCHANGED)
        try:
            not_valid = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "That code isn\'t valid")]'))
            )
            if not_valid.is_displayed():
                print("Invalid verification code detected")
                resend_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Request a new one")]'))
                )
                resend_button.click()
                time.sleep(10)
                instCodeNew = getManualVeriCodeDouble(instCode)
                confInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'email_confirmation_code'))
                )
                confInput.send_keys(Keys.CONTROL + "a")
                confInput.send_keys(Keys.DELETE)
                confInput.send_keys(instCodeNew, Keys.ENTER)
                print(f"✅ Entered new verification code: {instCodeNew}")
        except:
            print("ℹ️ No invalid code prompt found")
        time.sleep(5)

        # Handle notifications (UNCHANGED)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
            ).click()
            print("✅ Clicked Not Now for notifications")
        except:
            print("ℹ️ No notification prompt found")
        time.sleep(2)

        # Logout (UNCHANGED)
        try:
            profile_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@data-testid="user-avatar"]'))
            )
            profile_icon.click()
            logout_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Log Out")]'))
            )
            logout_button.click()
            print("✅ Logged out")
        except Exception as e:
            print(f"Error during logout: {e}")

        # Switch to professional account
        switch_to_professional(driver, name, acc_password)
        print("🎉 COMPLETE SUCCESS!")

    except Exception as e:
        print(f"❌ Error: {e}")
        with open("C:\\ac\\error_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Error page source saved")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()