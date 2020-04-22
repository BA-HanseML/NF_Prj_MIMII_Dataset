print('load audition_function_akkuplot')

#TODO fix the hue transform to list of hue
#TODO use diffrent color map 
#TODO adjust line with based on amount of lines in the plot
class audition_akku_plot():
    def __init__(self, xlabel='x', ylabel='y'):
        self.y=[]
        self.name=[]
        self.x=[]
        self.hue_info=[]
        self.xlabel=xlabel
        self.ylabel=ylabel
        
    def plot(self,hue=True): # if hue is False plot legend by name
        # color map
        cmap_u = cm.get_cmap(name='viridis', lut=None)
        c_set = set(self.hue_info)
        c_set_l = list(c_set)
        c_set_c = np.linspace(0,1,len(c_set_l))
        print(c_set_c,c_set_l, len(self.x), len(self.x[2]), len(self.x[0]))
        for i in range(len(self.x)):
            #print(i)
            x = self.x[i]
            y = self.y[i]
            n = self.name[i]
            h = self.hue_info[i]
            if hue:
                if len(c_set_l)>1:
                    c = cmap_u(c_set_c[h])
                else:
                    c = 'b'
                
            plt.plot(x,y,label=h,color=c) # todo 
            
        plt.xlabel(self.xlabel) 
        plt.ylabel(self.ylabel) 
        plt.grid()
        #plt.legend()
        # https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/custom_legends.html

    
    def add_line(self,x,y,name,hue_info):
        self.y.append(y)
        self.x.append(x)
        self.name.append(name)
        self.hue_info.append(hue_info)