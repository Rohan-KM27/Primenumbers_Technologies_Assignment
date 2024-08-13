from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the path to the ChromeDriver executable
service = Service('/path/to/chromedriver')  # Replace with your actual path
driver = webdriver.Chrome(service=service)
driver.get("https://hprera.nic.in/PublicDashboard")

try:
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")[1:7]

    def get_project_details(detail_url):
        driver.get(detail_url)
        gstin = driver.find_element(By.XPATH, "//td[text()='GSTIN No']/following-sibling::td").text.strip()
        pan = driver.find_element(By.XPATH, "//td[text()='PAN No']/following-sibling::td").text.strip()
        name = driver.find_element(By.XPATH, "//td[text()='Name']/following-sibling::td").text.strip()
        address = driver.find_element(By.XPATH, "//td[text()='Permanent Address']/following-sibling::td").text.strip()
        return {
            "GSTIN No": gstin,
            "PAN No": pan,
            "Name": name,
            "Permanent Address": address
        }

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        project_name = cells[1].text.strip()
        rera_number = cells[2].text.strip()
        detail_url = "https://hprera.nic.in" + cells[2].find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        print(f"Project Name: {project_name}")
        print(f"RERA Number: {rera_number}")
        
        project_details = get_project_details(detail_url)
        for key, value in project_details.items():
            print(f"{key}: {value}")
        
        print("\n" + "-"*50 + "\n")

finally:
    driver.quit()
