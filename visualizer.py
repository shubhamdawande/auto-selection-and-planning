import tkinter
import time
import tkFont
from globals import *

## View layouts on 2d canvas using tkinter gui
def render_layouts(generation_costs, historic):

    # tkinter parameters
    scale = 20
    root = tkinter.Tk()
    root.geometry("800x800")
    canvas = tkinter.Canvas(root, bg='green', width=scale*room_dimensions['width'], height=scale*room_dimensions['depth'])
    canvas.pack()

    for gen_index in range(n_generations - 2, n_generations - 1):
        
        for i in range(0, population_size):

            layout = historic[gen_index][i]
            #print generation_costs[gen_index][layout.items()[0][0]]
                
            if generation_costs[gen_index][layout.items()[0][0]] == 0:

                #print "Plotting layout....."
                asset_list = layout.items()[0][1]
                for asset in asset_list:
                    
                    #print "\nasset position:", asset[1]
                    #print "asset rotation:", asset[2]
                    #print asset[0]._dimension

                    asset[1] = {'x' : asset[1]['x'], 'z' : room_dimensions['depth'] - asset[1]['z']}

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
                                       font=tkFont.Font(family='Helvetica', size=6),
                                       text="%s"%asset[0]._vertical)
                
                # show total cost
                canvas.create_text(scale * room_dimensions['width']/2, 10, fill="yellow",
                                       font=tkFont.Font(family='Helvetica', size=10),
                                       text="%s, cost: %s"%(i, generation_costs[gen_index][layout.items()[0][0]]))

                root.update()
                #print "debug:", i
                #raw_input('Press enter to continue: ')
                time.sleep(1)
                canvas.delete("all")
    
    root.mainloop()
