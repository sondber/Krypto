import pip
def install(package):
    pip.main(['install', package])

install('tabulate')

from tabulate import tabulate

table = [["Sun",696000,1989100000],["Earth",6371,5973.6],["Moon",1737,73.5],["Mars",3390,641.85]]

print(tabulate(table, headers="true",tablefmt="latex"))