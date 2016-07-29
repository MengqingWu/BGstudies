import ROOT
import sys
from array import array
import pickle
from PlotterBase import PlotterBase
class MergedPlotter(PlotterBase):

    def __init__(self,plotters):
        super(MergedPlotter,self).__init__()
        self.plotters=plotters
        self.corrFactors=plotters[0].corrFactors

    def applySmoothing(self):
        for plotter in self.plotters:
            plotter.applySmoothing()


    def drawTH1(self,name,var,cuts,lumi,bins,mini,maxi,titlex = "", titley="", units = "",drawStyle = "HIST"):
        h=None
        plotterCount=0
        for plotter in self.plotters:
            hname=name+str(plotterCount)
            if h is None:
                h=plotter.drawTH1(hname,var,cuts,lumi,bins,mini,maxi,titlex,units,drawStyle)
            else:
                h.Add(plotter.drawTH1(hname,var,cuts,lumi,bins,mini,maxi,titlex,units,drawStyle))
            plotterCount+=1
                
        h.SetLineColor(self.linecolor)
        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        h.GetXaxis().SetTitle(titlex)
        if titley:      h.GetYaxis().SetTitle(titley)
        if units != '': h.GetXaxis().SetTitle(titlex+ " ("+units+")")
        return h

    def drawTH2(self,name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,titlex = "",unitsx = "",titley = "",unitsy = "",drawStyle = "COLZ"):
        h=None
        for plotter in self.plotters:
            if h is None:
                h=plotter.drawTH2(name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,titlex,unitsx,titley,unitsy,drawStyle)
            else:
                h.Add(plotter.drawTH2(name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,titlex,unitsx,titley,unitsy,drawStyle))

#        h.SetLineStyle(self.linestyle)
#        h.SetLineColor(self.linecolor)
#        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        if unitsx: titlex+=" ["+unitsx+"]"
        if unitsy: titley+=" ["+unitsy+"]"
        h.GetXaxis().SetTitle(titlex)
        h.GetYaxis().SetTitle(titley)
        return h


    def drawProfile(self,name,var,cuts,lumi,binsx,minx,maxx,miny,maxy,titlex = "",unitsx = "",titley = "",unitsy = "",drawStyle = "COLZ"):
        h=None
        for plotter in self.plotters:
            if h is None:
                h=plotter.drawProfile(name,var,cuts,lumi,binsx,minx,maxx,miny,maxy,titlex,unitsx,titley,unitsy,drawStyle)
            else:
                h.Add(plotter.drawProfile(name,var,cuts,lumi,binsx,minx,maxx,miny,maxy,titlex,unitsx,titley,unitsy,drawStyle))

#        h.SetLineStyle(self.linestyle)
#        h.SetLineColor(self.linecolor)
#        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        h.GetXaxis().SetTitle(titlex+ " ["+unitsx+"]")
        h.GetYaxis().SetTitle(titley+ " ["+unitsy+"]")
        return h


    def drawTH3(self,name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,binsz,minz,maxz,titlex = "",unitsx = "",titley = "",unitsy = "",drawStyle = "COLZ"):
        h=None
        for plotter in self.plotters:
            if h is None:
                h=plotter.drawTH3(name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,binsz,minz,maxz,titlex,unitsx,titley,unitsy,drawStyle)
            else:
                h.Add(plotter.drawTH3(name,var,cuts,lumi,binsx,minx,maxx,binsy,miny,maxy,binsz,minz,maxz,titlex,unitsx,titley,unitsy,drawStyle))

        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        h.GetXaxis().SetTitle(titlex+ " ["+unitsx+"]")
        h.GetYaxis().SetTitle(titley+ " ["+unitsy+"]")
        return h


    def drawTH2Binned(self,name,var,cuts,lumi,binningx,binningy,titlex = "",unitsx = "",titley = "",unitsy = "",drawStyle = "COLZ"):
        h=None
        for plotter in self.plotters:
            if h is None:
                h=plotter.drawTH2Binned(name,var,cuts,lumi,binningx,binningy,titlex,unitsx,titley,unitsy,drawStyle)
            else:
                h.Add(plotter.drawTH2Binned(name,var,cuts,lumi,binningx,binningy,titlex,unitsx,titley,unitsy,drawStyle))

#        h.SetLineStyle(self.linestyle)
#        h.SetLineColor(self.linecolor)
#        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        h.GetXaxis().SetTitle(titlex+ " ["+unitsx+"]")
        h.GetYaxis().SetTitle(titley+ " ["+unitsy+"]")
        return h

    def drawTH2Binnedv1(self,name,var,cuts,lumi,binsx,minx,maxx,binningy,titlex = "",unitsx = "",titley = "",unitsy = "",drawStyle = "COLZ"):
        h=None
        for plotter in self.plotters:
            if h is None:
                h=plotter.drawTH2Binnedv1(name,var,cuts,lumi,binsx,minx,maxx,binningy,titlex,unitsx,titley,unitsy,drawStyle)
            else:
                h.Add(plotter.drawTH2Binnedv1(name,var,cuts,lumi,binsx,minx,maxx,binningy,titlex,unitsx,titley,unitsy,drawStyle))

#        h.SetLineStyle(self.linestyle)
#        h.SetLineColor(self.linecolor)
#        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        if unitsx: titlex+=" ["+unitsx+"]"
        if unitsy: titley+=" ["+unitsy+"]"
        h.GetXaxis().SetTitle(titlex)
        h.GetYaxis().SetTitle(titley)
        return h

    def drawTH1Binned(self,name,var,cuts,lumi,binningx,titlex = "",unitsx = "",drawStyle = "COLZ"):
        h=None
        plotterCount=0
        for plotter in self.plotters:
            hname=name+str(plotterCount)
            if h is None:
                h=plotter.drawTH1Binned(hname,var,cuts,lumi,binningx,titlex,unitsx,drawStyle)
            else:
                h.Add(plotter.drawTH1Binned(hname,var,cuts,lumi,binningx,titlex,unitsx,drawStyle))
            plotterCount+=1

        h.SetLineColor(self.linecolor)
        h.SetLineWidth(self.linewidth)
        h.SetFillStyle(self.fillstyle)
        h.SetFillColor(self.fillcolor)
        h.SetMarkerStyle(self.markerstyle)
        h.GetXaxis().SetTitle(titlex)
        if unitsx: titlex+=" ["+unitsx+"]"
        h.GetXaxis().SetTitle(titlex)
        return h

