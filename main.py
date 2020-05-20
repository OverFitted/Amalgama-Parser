from Parser import Parser

if __name__ == '__main__':
    link = "https://www.amalgama-lab.com/songs/t/tones_and_i/dance_monkey.html"
    parser = Parser(link)
    parser.save()
