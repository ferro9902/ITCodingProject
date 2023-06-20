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

print("total estimated time = ", path[-1].get_full_weight())

for obj in path:
    print(obj)
