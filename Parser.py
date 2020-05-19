import bs4
import pandas
from requests import get


class Parser:
    def __init__(self, link):
        self.link = link
        self.name = str()
        self.text = None

    def get_name(self):
        self.name = " ".join(self.link.split("/")[-1].replace(".html", "").split("_"))  # Getting sound name
        return self.name.capitalize()

    def get_text(self):
        req = get(self.link)  # Getting URL content

        page_text = bs4.BeautifulSoup(req.text, features="lxml").text  # Parsing HTML code to text
        page_text = page_text[page_text.find("оригинал"):][:-80]  # Removing "pre"text
        page_text = page_text[page_text.find(")") + 1:]  # Removing sound name
        page_text = page_text[page_text.find(")") + 4:]

        if page_text.find("* поэтический перевод") != -1:  # Checking if song has poetic translation
            page_text = page_text[:-24]

        if page_text.find("(перевод") != -1:  # Checking if song has additional translation
            page_text = page_text[:page_text.find("(перевод")].split("\n")
            page_text = page_text[:-10]
        else:
            page_text = page_text.split("\n")

        self.text = [x for x in page_text if x]

        return self.text

    def save(self, file_name=None):
        if not file_name:  # Checking if got name
            if not self.name:
                self.get_name()
            file_name = self.name
        if file_name.find("csv") == -1:  # Adding .csv if needed
            file_name += ".csv"

        if not self.text:  # Checking if got text
            self.get_text()

        rus = list()
        eng = list()
        for i in range(len(self.text)):  # Getting text by languages
            j = self.text[i]
            if i % 2:
                rus.append(j)
            else:
                eng.append(j)

        df = pandas.DataFrame(list(zip(eng, rus)), columns=["Rus", "Eng"])  # Making DF and saving text to it
        df.to_csv(f"CSV/{file_name}")

        return 0
