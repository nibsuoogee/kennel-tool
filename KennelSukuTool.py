from urllib.request import urlopen
from lxml import html
from lxml.cssselect import CSSSelector
sel = CSSSelector('div.content')
from time import sleep

class Dog:
    def __init__(self, name, generation):
        self.name = name
        self.generation = generation

rowspan_to_generation = {
    '128': 1,
    '64': 2,
    '32': 3,
    '16': 4,
    '8': 5,
    '4': 6,
    '2': 7,
    '1': 8
}

print("\nTervetuloa KennelSukuTool -työkaluun\n")
print("Liitä leikepöydältä koirien hakutulosten URL osoitteet.")
print("HUOM. ennen URL:n kopioimista, aseta sukupolvien lukumäärä arvoon 8 sukutaulukon yläpuolelta.\n")

print("Ctrl + C päättää ohjelman jos se jostain syystä jumiutuu.")
url1 = ''
while(url1 != '0'):
    url1 = ''
    url2 = ''
    urls = []
    ancestor_lists = []

    url1 = str(input("\nLiitä koiran 1 URL (0 päättää ohjelman): "))
    if (url1 == '0'):
        break
    url2 = str(input("Liitä koiran 2 URL (0 päättää ohjelman): "))
    if (url2 == '0'):
        break
    print("Etsin...")
    urls.append(url1)
    urls.append(url2)

    for url in urls:
        ancestors = []
        try:
            page = urlopen(url)
            html_bytes = page.read()
            html_content = html_bytes.decode("utf-8")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        tree = html.fromstring(html_content)

        td_class = "Sukutaulu"
        table_id = "tblSukutaulu"
        table = tree.cssselect(f"table#{table_id}")[0]
        td_elements = table.cssselect(f"a")

        if td_elements:
            for e in td_elements:
                a_text = ' '.join(e.xpath(".//text()")).strip()
                a_text_without_small = e.xpath("string(.)").strip()

                closest_td = e.xpath("ancestor::td")[0]
                rowspan_value = closest_td.get("rowspan", "1")

                generation = 0
                # If Generations (Sukupolvet) is not set by the page visitor,
                # gen 1 is detected by a rowspan of 8
                # gen 2 = rowspan 4
                # gen 3 = rowspan 2...

                # If it is set correctly to 8,
                # gen 1 = rowspan 128
                # gen 2 = rowspan 64
                # gen 3 = rowspan 32...
                substring = "Sukupolvet="
                index = url.find(substring)
                if index != -1 and index + len(substring) < len(url):
                    page_gen = int(url[index+len(substring)])
                    generation = rowspan_to_generation[rowspan_value] - (8 - page_gen)
                else:
                    generation = rowspan_to_generation[rowspan_value] - 4

                dog = Dog(a_text_without_small, generation)
                ancestors.append(dog)
            ancestor_lists.append(ancestors)
        else:
            print("An unexpected error occurred")
            exit()

    # Create sets of names from each list
    names_set1 = {dog.name for dog in ancestor_lists[0]}
    names_set2 = {dog.name for dog in ancestor_lists[1]}

    # Find common names
    common_names = names_set1.intersection(names_set2)

    common_objects_list1 = []
    common_objects_list2 = []

    # Iterate through the common names and find the match with the lowest generation number
    for name in common_names:
        # Find the objects with the common name in both lists
        common_objects_list1.extend([dog for dog in ancestor_lists[0] if dog.name == name])
        common_objects_list2.extend([dog for dog in ancestor_lists[1] if dog.name == name])

    # Find the minimum generation number in list1
    min_generation_list1 = min((dog.generation for dog in common_objects_list1), default=None)
    min_generation_obj_list1 = [dog for dog in common_objects_list1 if dog.generation == min_generation_list1]

    min_generation_list2 = min((dog.generation for dog in common_objects_list2), default=None)
    min_generation_obj_list2 = [dog for dog in common_objects_list2 if dog.generation == min_generation_list2]

    print("\nSukupolviltaan nuorimmat yhteiset vanhemmat:\n")
    print("Koira 1 yhteiset vanhemmat:")
    if (not min_generation_list1):
        print("      Ei yhteisiä sukupolvia (8 sukupolven etäisyydellä)")
    for obj in min_generation_obj_list1:
        print(f"   - ", end="")
        print(f"{obj.name}")
        print(f"     ({obj.generation}) suhteellista sukupolvea sitten.")

    print("\nKoira 2 yhteiset vanhemmat:")
    if (not min_generation_list2):
        print("      Ei yhteisiä sukupolvia (8 sukupolven etäisyydellä)")
    for obj in min_generation_obj_list2:
        print(f"   - ", end="")
        print(f"{obj.name}")
        print(f"     ({obj.generation}) suhteellista sukupolvea sitten.")

print("\nKiitos ohjelman käytöstä.")
print("Elias Syyrilä 2024")
sleep(4)