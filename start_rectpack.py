from rectpack import newPacker

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle



rectangles = [(300, 150, 0, 90, 0, 90), (270, 150, 0, 90, 0, 90), (250, 150, 0, 90, 0, 90),
(300, 150, 0, 90, 0, 90), (270, 150, 0, 90, 0, 90), (250, 150, 0, 90, 0, 90),
(300, 150, 0, 90, 0, 90), (270, 150, 0, 90, 0, 90), (250, 150, 0, 90, 0, 90),
(300, 150, 0, 90, 0, 90), (270, 150, 0, 90, 0, 90), (250, 150, 0, 90, 0, 90)]
bins = [(1000, 1000)]

packer = newPacker()

# Add the rectangles to packing queue
for r in rectangles:
	packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in bins:
	packer.add_bin(*b)

# Start packing
print packer._is_everything_ready()
packer.pack()

print packer[0]
# Obtain number of bins used for packing
nbins = len(packer)

# Index first bin
abin = packer[0]

# Bin dimmensions (bins can be reordered during packing)
width, height = abin.width, abin.height

# Number of rectangles packed into first bin
nrect = len(packer[0])
print packer[0].used_area()/(bins[0][0]*bins[0][1]+0.0)
print nrect

fig = plt.figure(figsize=(5, 5))
clear = max(bins[0])*0.1
tot_size = clear+max(bins[0])
currentAxis = fig.add_subplot(1,1,1)
currentAxis.set(xlim=(-clear,tot_size ), ylim=(-clear, tot_size))
currentAxis.add_patch(Rectangle((0,0), bins[0][0], bins[0][1],linewidth=2,edgecolor='r', alpha=1, facecolor='none'))
for pod in packer[0]:
    print pod
    currentAxis.add_patch(Rectangle((pod.x,pod.y), pod.width, pod.height,linewidth=1,edgecolor='b', alpha=0.5))
    #currentAxis.add_patch(Rectangle((pod.x+45,pod.y+45), pod.width-90, pod.height-90,linewidth=0.5,edgecolor='b', alpha=0.1))
    #currentAxis.add_patch(Rectangle((pod.x+90,pod.y+90), pod.width-180, pod.height-180,linewidth=0.5,edgecolor='b', alpha=0.1))
plt.show()
