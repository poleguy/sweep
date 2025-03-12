#git clone git@github.com:florianfesti/boxes.git
#python setup.py install 
#step one copy boxes/generators/electronicsbox.py or cardbox.py




#use tests/test_svg.py as a tutorial for now.

#pip install qrcode lxml
#pytest

#to see if it passes. yup. everything is installed okay.

#initial setup window didn't work. it was mixing pytest python3.11 and python3.12 somehow.

#python
import boxes
import boxes.generators
from pathlib import Path



class Spring(boxes.Boxes):
    """Cut a pair of spring slots into it"""

    ui_group = "Part"

    def __init__(self) -> None:        
        boxes.Boxes.__init__(self)
        #self.addSettingsArgs(boxes.edges.FlexSettings)
        self.buildArgParser("x", "y")
        

    def render(self):
        x, y = self.x, self.y

        self.moveTo(5, 5)
        # first side
        self.edge(6)
        # todo: how to add an edge type
        #self.edges["X"](x, y)
        #self.edges["t"](x)
        #self.edge(x)

        depth = 8
        offset = 0
        angle = 88
        tip = 0.5
        self.corner(angle)
        self.edge(offset)
        for i in range(3):
            
            self.edge(depth)
            self.corner(-angle)
            self.edge(tip)
            self.corner(-angle)
            self.edge(depth)
            self.corner(angle)
            self.edge(3)
            self.corner(angle)

        self.edge(depth)
        self.corner(-angle)
        self.edge(tip)
        self.corner(-angle)
        self.edge(depth+offset)
        self.corner(angle)
        self.edge(tip)



        self.edge(1) # end extension bottom
        self.corner(90)
        self.edge(y)
        # other side
        self.corner(90)
        
        self.edge(1+2.5) # end extension + offset to align with bottom edge
        #self.edge(x + 9)
        self.corner(angle)
        self.edge(offset)
        for i in range(3):
            
            self.edge(depth)
            self.corner(-angle)
            self.edge(tip)
            self.corner(-angle)
            self.edge(depth)
            self.corner(angle)
            self.edge(3)
            self.corner(angle)

        self.edge(depth)
        self.corner(-angle)
        self.edge(tip)
        self.corner(-angle)
        self.edge(depth+offset)
        self.corner(angle)
        self.edge(tip)
        
        
        self.corner(90)
        self.edge(y)
        self.corner(90)


class InsetEdgeSettings(boxes.edges.Settings):
    """Settings for InsetEdge"""
    absolute_params = {
        "thickness": 0,
    }


class InsetEdge(boxes.edges.BaseEdge):
    """An edge with space to slide in a lid"""
    def __call__(self, length, **kw):
        t = self.settings.thickness
        self.corner(90)
        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(length, tabs=2)
        self.corner(-90)
        self.edge(t, tabs=2)
        self.corner(90)
        


class InsetFingerEdge(boxes.edges.BaseEdge):
    """An edge with fingers to grab a slid in lid"""
    def __call__(self, length, **kw):
        t = self.settings.thickness
        #self.edge(t, tabs=2)
        
        #self.edge(length, tabs=2)
        self.edges["F"](length, tabs=2)
        #self.edge(t, tabs=2)



class SupportEdgeSettings(boxes.edges.Settings):
    """Settings for InsetEdge"""
    absolute_params = {
        "thickness": 0,
        "depth_factor": 2.0,
        "reversed": False # put the remainder at the front
    }


class SupportEdgeSingle(boxes.edges.BaseEdge):
    """A single toothed edge with no teeth at either edge.
    To not complicate usual general case.
    """
    def __call__(self, length, **kw):
        # depth is for depth of cut
        t = self.settings.thickness
        depth_factor = self.settings.depth_factor

        remainder = t  # extra length needed to fill

        # add gap an tooth
        self.edge(t, tabs=2) # gap
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)  
        self.corner(90)
        self.edge(t, tabs=2) # tooth
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)

        # end low
        self.edge(t, tabs=2) # gap
        

class SupportEdge(boxes.edges.BaseEdge):
    """A toothed edge with no teeth at either edge"""
    def __call__(self, length, **kw):
        # depth is for depth of cut
        t = self.settings.thickness
        depth_factor = self.settings.depth_factor
        reversed = self.settings.reversed

        count = int(length/(t*2))

        remainder = length - (count-1)*t*2

        # if we can fit one more in and still be low at the end for a length of t, do so
        # with tolerance
        if remainder > t*3 - t/100:
            count+=1
            remainder -= t*2


        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        if not reversed:
            self.edge(remainder, tabs=2)  # stretch the high edge so the end one is tight
        else:
            self.edge(t, tabs=2) 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)


        for i in range(count-3):
            self.edge(t, tabs=2)
            self.corner(-90)
            self.edge(t*depth_factor, tabs=2)
            self.corner(90)
            self.edge(t, tabs=2)
            self.corner(90)
            self.edge(t*depth_factor, tabs=2)
            self.corner(-90)


        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        if reversed:
            self.edge(remainder, tabs=2)  # stretch the high edge so the end one is tight
        else:
            self.edge(t, tabs=2) 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)

        # end low
        self.edge(t, tabs=2)


class SupportEdgeHoldDown(boxes.edges.BaseEdge):
    """A toothed edge with teeth at either edge, and a double tooth at the middle
    To hold down one or two PCBs and clear components.
    """
    def __call__(self, length, **kw):
        # depth is for depth of cut
        t = self.settings.thickness
        depth_factor = self.settings.depth_factor
        

        half = length/2

        gap_width = half - t*4 # double wide tooth at either end of either half

        # start with tooth
        self.edge(t*2, tabs=2) #double wide tooth 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)        
        
        self.edge(gap_width, tabs=2) # gap
        
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        self.edge(t*2*2, tabs=2) #double-double wide tooth 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)
        
        self.edge(gap_width, tabs=2) # gap

        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        self.edge(t*2, tabs=2) #double wide tooth 



class SupportEdgeOdd(boxes.edges.BaseEdge):
    """A toothed edge with teeth right at either edge to press on sides"""
    def __call__(self, length, **kw):
        # depth is for depth of cut
        t = self.settings.thickness
        depth_factor = self.settings.depth_factor
        reversed = self.settings.reversed


        count = int(length/(t*2))

        remainder = length - (count-1)*t*2

        # if we can fit one more in and still be low at the end for a length of t, do so
        # with tolerance
        if remainder > t*3 - t/100:
            count+=1
            remainder -= t*2


        #if not odd:
        #    self.edge(t, tabs=2)
        #self.corner(-90)
        #self.edge(t*depth_factor, tabs=2)
        #self.corner(90)
        if not reversed:
            self.edge(remainder, tabs=2)  # stretch the high edge so the end one is tight
        else:
            self.edge(t, tabs=2) 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)


        for i in range(count-3):
            self.edge(t, tabs=2)
            self.corner(-90)
            self.edge(t*depth_factor, tabs=2)
            self.corner(90)
            self.edge(t, tabs=2)
            self.corner(90)
            self.edge(t*depth_factor, tabs=2)
            self.corner(-90)


        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        if reversed:
            self.edge(remainder, tabs=2)  # stretch the high edge so the end one is tight
        else:
            self.edge(t, tabs=2) 
        self.corner(90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(-90)

        # end low
        #if not odd:
        #    self.edge(t, tabs=2)
        #else:
        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(t*depth_factor, tabs=2)
        self.corner(90)
        self.edge(t, tabs=2)
        #self.corner(90)
        #self.edge(t, tabs=2)
        #self.corner(-90)
        
        #self.edge(t*depth_factor, tabs=2)
        #self.corner(90)




class ElectronicsSlideBox(boxes.Boxes):
    """Closed box with screw on top and mounting holes"""

    ui_group = "Box"

    def __init__(self) -> None:
        boxes.Boxes.__init__(self)
        self.addSettingsArgs(boxes.edges.FingerJointSettings)
        self.addSettingsArgs(boxes.edges.FlexSettings)
        self.buildArgParser("x", "y", "h")
        self.argparser.add_argument(
            "--triangle", action="store", type=float, default=25.,
            help="Sides of the triangles holding the lid in mm")
        self.argparser.add_argument(
            "--d1", action="store", type=float, default=2.,
            help="Diameter of the inner lid screw holes in mm")
        self.argparser.add_argument(
            "--d2", action="store", type=float, default=3.,
            help="Diameter of the lid screw holes in mm")
        self.argparser.add_argument(
            "--d3", action="store", type=float, default=3.,
            help="Diameter of the mounting screw holes in mm")
        self.argparser.add_argument(
            "--outsidemounts", action="store", type=boxes.boolarg, default=True,
            help="Add external mounting points")
        self.argparser.add_argument(
            "--holedist", action="store", type=float, default=7.,
            help="Distance of the screw holes from the wall in mm")

    #inner dimensions of surrounding box (disregarding inlays)
    @property
    def boxheight(self):
        #if self.outside:
        #    return self.h - 3 * self.thickness
        return self.h

    def wallxCB(self):
        t = self.thickness
        #self.fingerHolesAt(0, self.h-1.5*t, self.triangle, 0)
        #self.fingerHolesAt(self.x, self.h-1.5*t, self.triangle, 180)

    def wallxFrontCB(self):
        # opening for slide
        t = self.thickness
        #self.fingerHolesAt(0, self.h-1.5*t, self.triangle, 0)
        #self.fingerHolesAt(self.x, self.h-1.5*t, self.triangle, 180)

        y = self.boxheight

        pos = 0.5 * t
        pos += self.x + t
        #self.fingerHolesAt(pos, 0, y, 90)


    def wallyCB(self):
        t = self.thickness
        #self.fingerHolesAt(0, self.h-1.5*t, self.triangle, 0)
        #self.fingerHolesAt(self.y, self.h-1.5*t, self.triangle, 180)

    def render(self):

        t = self.thickness        
        x, y, h = self.x, self.y, self.h # all inside measurements
        d1, d2, d3 =self.d1, self.d2, self.d3
        hd = self.holedist
        tr = self.triangle
        trh = tr / 3.

        #if self.outside:
        #    self.x = x = self.adjustSize(x)
        #    self.y = y = self.adjustSize(y)
        #    self.h = h = h - 3*t



        s = InsetEdgeSettings(thickness=t)
        p = InsetEdge(self, s)
        p.char = "a"
        self.addPart(p)
        
        s = InsetEdgeSettings(thickness=t)
        p = InsetFingerEdge(self, s)
        p.char = "b"
        self.addPart(p)


        self.rectangularWall(x, h+t, "fFaF", callback=[self.wallxFrontCB],
                             move="right", label="Front Wall")
        self.rectangularWall(y, h+t, "ffFf", callback=[self.wallyCB],
                             move="up", label="Side Wall 1")
        self.rectangularWall(y, h+t, "ffFf", callback=[self.wallyCB],
                             label="Side Wall 2")
        self.rectangularWall(x, h+t, "fFeF", callback=[self.wallxCB],
                             move="left up", label="Back Wall")

        self.rectangularWall(y, t, "efee", move="up only")

        with self.saved_context():
            self.rectangularWall(y, t, "eefe", move="right", label="Lip Left")
            self.rectangularWall(y, t, "feee", move="right", label="Lip Right")
        
        self.rectangularWall(y, t * 2, "efee", move="up only")

        support_y_short = y
        support_y_tall = y
        support_x_short = x
        support_x_tall = x
        support_helper = 9
        support_helper_x2 = 15

        fill_factor = 0.3
        # print several of each
        support_x = int(y/t*fill_factor/2)*2 
        support_y = int(x/t*fill_factor/2)*2
        support_n = max(support_x,support_y) # more is better


        s = SupportEdgeSettings(thickness=t, depth_factor=1.0)
        p = SupportEdge(self, s)
        p.char = "A"
        self.addPart(p)

        s = SupportEdgeSettings(thickness=t, depth_factor=2.0)
        p = SupportEdge(self, s)
        p.char = "B"
        self.addPart(p)

        s = SupportEdgeSettings(thickness=t, depth_factor=1.0)
        p = SupportEdgeSingle(self, s)
        p.char = "a"
        self.addPart(p)


        for i in range(support_n):
            # https://florianfesti.github.io/boxes/html/api_navigation.html
            with self.saved_context(): # group tall ones for optimal printing
                self.rectangularWall(support_y_tall, t*2, "eeAe", move="right", label="y support tall")        
                self.rectangularWall(support_x_tall, t, "eeBe", move="right", label="x support tall") # use upside down
            self.rectangularWall(y, t * 3, "eeAe", move="up only")
        #self.rectangularWall(y, t * 3, "eeAe", move="up only")

        for i in range(support_x):
            with self.saved_context():            
                self.rectangularWall(support_y_short, t, "eeAe", move="right", label="y support short")
                self.rectangularWall(support_x_short, t, "eeAe", move="right", label="x support short") # use upside down
                
                self.rectangularWall(support_helper, t, "eeae", move="right", label="1 t")
                self.rectangularWall(support_helper_x2, t, "eeAe", move="right", label="2 t")
            self.rectangularWall(y, t * 2, "eeBe", move="up only")
        

        # hold downs around edges

        connector_x = 3
        target_pcb_thickness = 1.3 # at target compression (compromise between 1.0 and 1.5 of actual boards)
        support_short_thickness = 6
        # the wall will be shorter than nominal since material is removed.
        # It wil be able to compress the full 2mm down from the nominal.
        # so the range of compression should be 1mm-2mm below nominal.
        # let's target having it at almost full compression with a 1.5mm board 
        # and still some compression with a 1mm board.
        # It's easier to remove material with a file, saw, planer than add it.
        max_spring_compression = 2.0
        min_spring_compression = 0.2
        target_spring_compression = 1.0 # compression in mm with target pcb thickness (max is 1x depth of cut: 2mm) (half compressed)
        print(f"x y h {x} {y} {h}")        
        print(f"connector_x {connector_x}")
        print(f"support_short_thickness {support_short_thickness}")
        # h is defined as the inner dimensions of the box, so compensate 
        hold_down_height = h - target_pcb_thickness - connector_x - support_short_thickness + target_spring_compression
        print(f"hold down height {hold_down_height}")
        # at max limit, target limit, and minimum
        print(f"board thickness compression limits: {h-hold_down_height-connector_x-support_short_thickness+max_spring_compression:0.2f} {h-hold_down_height-connector_x-support_short_thickness:0.2f}")

        s = SupportEdgeSettings(thickness=t, depth_factor=2.0)
        p = SupportEdgeOdd(self, s)
        p.char = "B"
        self.addPart(p)


        s = SupportEdgeSettings(thickness=t, depth_factor=1.0)
        p = SupportEdgeHoldDown(self, s)
        p.char = "A"
        self.addPart(p)


        for i in range(4):            
            with self.saved_context():  
                #self.rectangularWall(y, hold_down_height, "eeee", move="right", label="end support y simple") # for size check
                self.rectangularSpring(y, hold_down_height, "Aeee", move="right", label="hold down y") # as simple as possible
                self.rectangularWall(y, t, "eeee", move="up only")
                self.rectangularWall(x-2*t, 3*t, "Beee", move="right", label="connector x") # short by 2*t to slide straight down from top and clear side lips.
            self.rectangularSpring(y, hold_down_height, move="up only")

        
        

        if not self.outsidemounts:
            self.rectangularWall(x, y, "FFFF", callback=[
            lambda:self.hole(hd, hd, d=d3)] *4, move="right",
            label="Bottom")
        else:
            self.flangedWall(x, y, edges="FFFF",
                             flanges=[0.0, 2*hd, 0., 2*hd], r=hd,
                             callback=[
                    lambda:self.hole(hd, hd, d=d3)] * 4, move='up',
                    label="Bottom")
        self.rectangularWall(x, y+t, "eeee", move='up', label="Top") # long enough to cover front lip




        #self.rectangularWall(x - t * .2, y, "eeFe", move="right", label="Lid")

        #self.rectangularWall(x - t * .2, t, "fEeE", move="up", label="Lid Lip")

        #self.rectangularTriangle(tr, tr, "ffe", num=4,
        #    callback=[None, lambda: self.hole(trh, trh, d=d1)])

    def slot(self, l,w):
        r = w/2
        self.corner(90)
        self.edge(l)
        self.corner(-180,r)
        self.edge(l)
        self.corner(90)

    def rectangularSpring(self, x, y, edges="FeAe",
                        ignore_widths=[],
                        holesMargin=None, holesSettings=None,
                        bedBolts=None, bedBoltSettings=None,
                        callback=None,
                        move=None,
                        label=""):
        """
        Rectangular wall for all kind of box like objects

        :param x: width
        :param y: height
        :param edges:  (Default value = "eeee") bottom, right, top, left
        :param ignore_widths: list of edge_widths added to adjacent edge
        :param holesMargin:  (Default value = None)
        :param holesSettings:  (Default value = None)
        :param bedBolts:  (Default value = None)
        :param bedBoltSettings:  (Default value = None)
        :param callback:  (Default value = None)
        :param move:  (Default value = None)
        :param label: rendered to identify parts, it is not meant to be cut or etched (Default value = "")
        """
        if len(edges) != 4:
            raise ValueError("four edges required")
        edges = [self.edges.get(e, e) for e in edges]
        #print(edges)
        edges += edges  # append for wrapping around
        overallwidth = x + edges[-1].spacing() + edges[1].spacing()
        overallheight = y + edges[0].spacing() + edges[2].spacing()

        if self.move(overallwidth, overallheight, move, before=True):
            return

        w = 2 # gap between spring arms
        
        bottom_extra = 3  # to cut away for clearance
        top_extra = 3 #to establish length
        offset = 12-w        
        half_offset = 6-w        

        min_height = offset+half_offset+w+bottom_extra+top_extra

        remainder = y - min_height

        slot_length = x - 6 # to make it even spacing in x and y
        
        bottom_extra += remainder

        if 7 not in ignore_widths:
            self.moveTo(edges[-1].spacing())
        self.moveTo(0, edges[0].margin())
        for i, l in enumerate((x, y, x, y)):
            self.cc(callback, i, y=edges[i].startwidth() + self.burn)
            e1, e2 = edges[i], edges[i + 1]
            if (2*i-1 in ignore_widths or
                2*i-1+8 in ignore_widths):
                l += edges[i-1].endwidth()
            if 2*i in ignore_widths:
                l += edges[i+1].startwidth()
                e2 = self.edges["e"]
            if 2*i+1 in ignore_widths:
                e1 = self.edges["e"]

            if i == 0 or i == 2: # bottom, top
                edges[i](l,
                     bedBolts=self.getEntry(bedBolts, i),
                     bedBoltSettings=self.getEntry(bedBoltSettings, i))
            elif i == 1:
                #self.edgeCorner(e1, e2, 90)
                self.edge(half_offset+bottom_extra)
                self.slot(slot_length,w)
                self.edge(offset+top_extra)
            elif i == 3:
                #self.edgeCorner(e1, e2, 90)
                self.edge(half_offset+top_extra)
                self.slot(slot_length,w)
                self.edge(offset+bottom_extra)

                        
            self.edgeCorner(e1, e2, 90)

        #self.render_flex(x,y,1, e1, e2, label="support y")    

        if holesMargin is not None:
            self.moveTo(holesMargin,
                        holesMargin + edges[0].startwidth())
            self.hexHolesRectangle(x - 2 * holesMargin, y - 2 * holesMargin, settings=holesSettings)

        self.move(overallwidth, overallheight, move, label=label)

    def rectangularWall2(self, x, y, edges="eeee",
                        ignore_widths=[],
                        holesMargin=None, holesSettings=None,
                        bedBolts=None, bedBoltSettings=None,
                        callback=None,
                        move=None,
                        label=""):
        """
        Rectangular wall for all kind of box like objects

        :param x: width
        :param y: height
        :param edges:  (Default value = "eeee") bottom, right, top, left
        :param ignore_widths: list of edge_widths added to adjacent edge
        :param holesMargin:  (Default value = None)
        :param holesSettings:  (Default value = None)
        :param bedBolts:  (Default value = None)
        :param bedBoltSettings:  (Default value = None)
        :param callback:  (Default value = None)
        :param move:  (Default value = None)
        :param label: rendered to identify parts, it is not meant to be cut or etched (Default value = "")
        """
        if len(edges) != 4:
            raise ValueError("four edges required")
        edges = [self.edges.get(e, e) for e in edges]
        print(edges)
        edges += edges  # append for wrapping around
        overallwidth = x + edges[-1].spacing() + edges[1].spacing()
        overallheight = y + edges[0].spacing() + edges[2].spacing()

        if self.move(overallwidth, overallheight, move, before=True):
            return

        if 7 not in ignore_widths:
            self.moveTo(edges[-1].spacing())
        self.moveTo(0, edges[0].margin())


        for i, l in enumerate((x, y, x, y)):
            self.cc(callback, i, y=edges[i].startwidth() + self.burn)
            e1, e2 = edges[i], edges[i + 1]
            if (2*i-1 in ignore_widths or
                2*i-1+8 in ignore_widths):
                l += edges[i-1].endwidth()
            if 2*i in ignore_widths:
                l += edges[i+1].startwidth()
                e2 = self.edges["e"]
            if 2*i+1 in ignore_widths:
                e1 = self.edges["e"]

            edges[i](l,
                     bedBolts=self.getEntry(bedBolts, i),
                     bedBoltSettings=self.getEntry(bedBoltSettings, i))
            self.edgeCorner(e1, e2, 90)

        if holesMargin is not None:
            self.moveTo(holesMargin,
                        holesMargin + edges[0].startwidth())
            self.hexHolesRectangle(x - 2 * holesMargin, y - 2 * holesMargin, settings=holesSettings)

        self.move(overallwidth, overallheight, move, label=label)


    def render_flex(self, x,y,w, e1, e2, label= ""):
        # a solt of length l, w
        # 
        bottom_extra = 6  # to cut away for clearance
        offset = 10-w        
        half_offset = 5-w        

        l = x - 5 # to make it even spacing in x and y
        

        #self.text(label, x/2, y/2, align="middle center", color=boxes.Color.ANNOTATIONS, fontsize=4)


        # starting going right.
        # 90 is a left hand turn
        #self.edge(x)
        #e1 = self.edges["e"]
        self.edges["F"](x) # to allow for easy trimming to clear components
        

        # right edge
        #self.corner(90)
        self.edgeCorner(e1, e2, 90)
        self.edge(half_offset+bottom_extra)
        self.slot(l,w)
        self.edge(offset)
        self.slot(l,w)
        self.edge(offset)

        # top edge
        #self.corner(90)
        self.edgeCorner(e1, e2, 90)
        #self.edge(x)
        #self.edges["e"](x)
        self.edges["A"](x)

        # left edge
        #self.corner(90)
        self.edgeCorner(e1, e2, 90)
        self.edge(half_offset)
        self.slot(l,w)
        self.edge(offset)
        self.slot(l,w)
        self.edge(offset+bottom_extra)
        
        
        # final corner
        #self.corner(90)
        self.edgeCorner(e1, e2, 90)

        # move to right edge 
        #self.moveTo(x+self.spacing,0)
        print("ack")


# this was hard to figure out because it has a side-effect of creating boxes.generators.electronicsbox
#boxes.generators.getAllBoxGenerators()
# this was hard to figure out. I kept trying box = boxes.genorators.electronicsbox() or other variations
#box = boxes.generators.electronicsslidebox.ElectronicsSlideBox()
box = ElectronicsSlideBox()
#box = boxes.generators.cardbox.CardBox()


# should these all be multiples of 3? of 6? of 6+3?
# 60/72 gives it 1/2 extra mm. but still has double wide teeth
# 63/75 gives 4/5 extra mm, which is an entire notch too far, but should still work.
# a little margin might be good, so long as it doesn't fall off the lip. Even 1mm lip should be enough.

# back to original dimensions to try to not waste the original print
# all inner dimensions:
box.parseArgs(["--x","59",
               "--y","70",
               "--h","39",   # 31 above board to clear headers and dupont cables. 1.5 for board thickness. 6 below board. .5 rounding up. 
               "--debug", "False"
               ])
#box.parseArgs("")
box.open()
box.render()
boxData = box.close()
print(boxData.__sizeof__())
#45977
file = Path('electronicsbox.svg')
file.write_bytes(boxData.getvalue())
#45879
#exit

#xdg-open electronixbox.svg


