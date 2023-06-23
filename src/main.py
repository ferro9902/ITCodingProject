import app.CoordinatesInputForm as Form
import app.PathFinder as PathFinder

# start
form = Form.CoordinatesInputForm()
form.create_form()

start_coord = form.start
dest_coord = form.dest

pf = PathFinder.PathFinder(start_coord, dest_coord)
pf.resolve()
path = pf.get_shortest_path()

seconds = path[-1].get_full_weight()
hours = round(seconds // 3600)
minutes = round((seconds % 3600) // 60)
seconds = round(seconds % 60)

print(
    f"total estimated time {hours} hours, {minutes} minutes and {seconds} seconds")

for obj in path:
    print(obj)
