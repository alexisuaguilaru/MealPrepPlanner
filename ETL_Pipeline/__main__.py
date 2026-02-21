import asyncio
from ETL_Pipeline import MainAllrecipes

if __name__ == "__main__":

    recipes_allrecipes = MainAllrecipes()
    print(*recipes_allrecipes,sep='\n')