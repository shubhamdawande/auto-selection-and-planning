import tkinter as tk
import time
import tkFont as tf
from globals import *
from cost_function import calculate_cost

## View final generated layouts on 2d canvas using tkinter gui
def render_layouts(generation_costs, historic):

    # tkinter parameters
    scale = 20
    root = tk.Tk()
    root.geometry("800x800")
    canvas = tk.Canvas(root, bg='green', width=scale*room_dimensions['width'], height=scale*room_dimensions['depth'])
    canvas.pack()

    for gen_index in range(n_generations - 2, n_generations - 1):
        
        for i in range(0, population_size):
            layout = historic[gen_index][i]
            
            if generation_costs[gen_index][layout.items()[0][0]] == 0:
                asset_list = layout.items()[0][1]

                for asset in asset_list:
                    
                    print layout.items()[0][0]
                    print asset[0]._vertical
                    print asset[0]._dimension
                    print asset[2]
                    print asset[1]
                    #asset[1] = {'x' : asset[1]['x'], 'z' : room_dimensions['depth'] - asset[1]['z']}
                    print asset[1]

                    if asset[2] == 0 or asset[2] == 180: 
                        canvas.create_rectangle(scale*(asset[1]['x'] - asset[0]._dimension['depth'] / 2),
                        scale*(asset[1]['z'] - asset[0]._dimension['width'] / 2),
                        scale*(asset[1]['x'] + asset[0]._dimension['depth'] / 2),
                        scale*(asset[1]['z'] + asset[0]._dimension['width'] / 2),
                        fill='red')
                    else:
                        canvas.create_rectangle(scale * (asset[1]['x'] - asset[0]._dimension['width'] / 2),
                        scale * (asset[1]['z'] - asset[0]._dimension['depth'] / 2),
                        scale * (asset[1]['x'] + asset[0]._dimension['width'] / 2),
                        scale * (asset[1]['z'] + asset[0]._dimension['depth'] / 2),
                        fill='red')
                    
                    # show asset description
                    canvas.create_text(scale * asset[1]['x'], scale * asset[1]['z'], fill="darkblue",
                                       font=tf.Font(family='Helvetica', size=6),
                                       text="%s\n%s $"%(asset[0]._vertical, asset[0]._price))

                # show total fitness value and budget
                canvas.create_text(scale * room_dimensions['width']/2, 10, fill="yellow",
                                   font=tf.Font(family='Helvetica', size=10),
                                   text="%s, _id: %s, budget: %s $, cost: %s"%(i, layout.items()[0][0], budget, generation_costs[gen_index][layout.items()[0][0]]))

                root.update()
                #raw_input('Press enter to continue: ')
                time.sleep(1)
                canvas.delete("all")
    
    root.mainloop()


## Utility rendering function
def render_one(layout, room_dimensions, gen_count):
    
    cost = calculate_cost(layout, room_dimensions)

    if gen_count > 0:
        
        if cost == 0:

            # tkinter parameters
            scale = 20
            root = tk.Tk()
            root.geometry("800x800")
            canvas = tk.Canvas(root, bg='green', width=scale*room_dimensions['width'], height=scale*room_dimensions['depth'])
            canvas.pack()

            asset_list = layout.items()[0][1]

            #print "\nDEBUG ID:", len(asset_list)
            #count = 0
            for asset in asset_list:
            
                print layout.items()[0][0]
                print asset[0]._vertical
                print asset[0]._dimension
                print asset[2]
                print asset[1]
                #print count
                #count += 1
                
                asset[1] = {'x' : asset[1]['x'], 'z' : room_dimensions['depth'] - asset[1]['z']}
                print asset[1]

                if asset[2] == 0 or asset[2] == 180: 
                    canvas.create_rectangle(scale*(asset[1]['x'] - asset[0]._dimension['depth'] / 2),
                    scale*(asset[1]['z'] + asset[0]._dimension['width'] / 2),
                    scale*(asset[1]['x'] + asset[0]._dimension['depth'] / 2),
                    scale*(asset[1]['z'] - asset[0]._dimension['width'] / 2),
                    fill='red')
                else:
                    canvas.create_rectangle(scale * (asset[1]['x'] - asset[0]._dimension['width'] / 2),
                    scale * (asset[1]['z'] + asset[0]._dimension['depth'] / 2),
                            scale * (asset[1]['x'] + asset[0]._dimension['width'] / 2),
                            scale*(asset[1]['z'] - asset[0]._dimension['depth']/2), 
                            fill='red')
                            
                # show asset description
                canvas.create_text(scale * asset[1]['x'], scale * asset[1]['z'], fill="darkblue",
                                    font=tf.Font(family='Helvetica', size=6),
                                    text="%s\n%s $"%(asset[0]._vertical, asset[0]._price))

                # show total fitness value and budget
                canvas.create_text(scale * room_dimensions['width']/2, 10, fill="yellow",
                                    font=tf.Font(family='Helvetica', size=10),
                                    text="_id: %s, budget: %s $, cost: %s"%(layout.items()[0][0], budget, cost))

            root.update()
            #raw_input('Press enter to continue: ')
            time.sleep(1)
            root.destroy()
            return
        else:
            return
    else:
        return