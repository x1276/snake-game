import json
from rich import print

if __name__ == "__main__":
	with open("data.json", "r", encoding="utf8") as data:
	    content = json.load(data)
	    settings = content["settings"]
	    playerdata = content["player"]
	data.close()

	print(f"The current resolution of the game is [green]{settings['resolution']}[/green] (screen resolution of [green]{settings['resolution'][0] * 60}[/green]px by [green]{settings['resolution'][1] * 60}[/green]px)")
	if input("Would you like to change the values? (y/n)") in ["y", "1", "Y", "н", "Н", "Yes", "YES"]: settings["resolution"] = [int(input("Enter the new x value:")),int(input("Enter the new y value:"))]

	print(f"The current speed of the snake is [green]{settings['game-speed']}[/green]")
	if input("Would you like to change the speed? (y/n)") in ["y", "1", "Y", "н", "Н", "Yes", "YES"]: settings["game-speed"] = int(input("Enter the new value of the speed"))

	print(f"The current highscore is [green]{playerdata['highscore']}[/green]")
	if input("Would you like to reset the highscore? (y/n)") in ["y", "1", "Y", "н", "Н", "Yes", "YES"]:
		playerdata["highscore"] = 0
		print("[blue]Highscore[/blue] has been reset succsessfully!")

	print("The [blue]values[/blue] have been updated succsessfully! Press [blue]enter[/blue] to exit and save the changes")
	input()

	with open("data.json", "w", encoding="utf8") as data:
		new_data = {
			"settings" : settings,
			"player" : playerdata
		}
		data.write(str(new_data).replace("'", "\""))
	data.close()