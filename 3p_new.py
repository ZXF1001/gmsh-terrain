import gmsh
import numpy as np

gmsh.initialize()
gmsh.model.add("my_model")

# n行m列的矩阵，代表dem数据
zlist = np.load("terrain.npy")
zlist
x_dist = 11252.55935707817 # x方向的总间距
y_dist = 9608.555047642712 # y方向的总间距
lc1 = 50; # 近地面边界层网格尺寸
lc2 = 300; # 远离地面边界层网格尺寸
zMax = zlist.max() + 2000; # 最大高度
zLayer = 20; # 边界层厚度

zlist += zLayer #todo: 注释解释一下为什么要加zLayer
dx = x_dist / (zlist.shape[1] - 1) # x方向的间距
dy = y_dist / (zlist.shape[0] - 1) # y方向的间距

tol_x = dx / 10
tol_y = dy / 10

zlist = np.flipud(zlist)
n = zlist.shape[0]
m = zlist.shape[1]
# 创建两个空的数组，形状和zlist一样n行m列
# 储存下面上每个格点的tag序号
plist_lower = np.zeros((n, m)).astype(int)

# 创建代表底面上平行于x轴的线段的tag序号的数组
# 形状为n行m-1列
llist_x_lower = np.zeros((n, m - 1)).astype(int)
# 创建代表底面上平行于y轴的线段的tag序号的数组
# 形状为n-1行m列
llist_y_lower = np.zeros((n - 1, m)).astype(int)

# 创建代表底面上的线环的tag序号的数组
# 形状为n-1行m-1列
llist_loop_lower = np.zeros((n - 1, m - 1)).astype(int)
# 创建代表底面上的面的tag序号的数组
# 形状为n-1行m-1列
slist_lower = np.zeros((n - 1, m - 1)).astype(int)

factory = gmsh.model.occ

for n_row, row in enumerate(zlist):
    for n_col, z in enumerate(row):
        plist_lower[n_row][n_col] = factory.addPoint(n_col*dx, n_row*dy, z, lc1)

upper_p00_index = factory.addPoint(0, 0, zMax, lc2)
upper_p10_index = factory.addPoint((m-1)*dx, 0, zMax, lc2)
upper_p11_index = factory.addPoint((m-1)*dx, (n-1)*dy, zMax, lc2)
upper_p01_index = factory.addPoint(0, (n-1)*dy, zMax, lc2)


# 平行于x轴的线
for n_row, row in enumerate(llist_x_lower):
    for n_col, p_index in enumerate(row):
        llist_x_lower[n_row][n_col] = factory.addLine(plist_lower[n_row][n_col], plist_lower[n_row][n_col + 1])
## 顶上的线
llist_x_upper_0 = factory.addLine(upper_p00_index, upper_p10_index)
llist_x_upper_1 = factory.addLine(upper_p01_index, upper_p11_index)

# 平行于y轴的线
for n_row, row in enumerate(llist_y_lower):
    for n_col, p_index in enumerate(row):
        llist_y_lower[n_row][n_col] = factory.addLine(plist_lower[n_row][n_col], plist_lower[n_row + 1][n_col])
## 顶上的线
llist_y_upper_0 = factory.addLine(upper_p00_index, upper_p01_index)
llist_y_upper_1 = factory.addLine(upper_p10_index, upper_p11_index)

# 平行于z轴的线
llist_z_00 = factory.addLine(plist_lower[0][0], upper_p00_index)
llist_z_10 = factory.addLine(plist_lower[0][-1], upper_p10_index)
llist_z_11 = factory.addLine(plist_lower[-1][-1], upper_p11_index)
llist_z_01 = factory.addLine(plist_lower[-1][0], upper_p01_index)

# 创建底面的线环和面
for n_row, row in enumerate(llist_loop_lower):
    for n_col, p_index in enumerate(row):
        llist_loop_lower[n_row][n_col] = factory.addCurveLoop(
            [llist_x_lower[n_row][n_col],
             llist_y_lower[n_row][n_col + 1],
             -llist_x_lower[n_row + 1][n_col],
             -llist_y_lower[n_row][n_col]]
             )
        slist_lower[n_row][n_col] = factory.addSurfaceFilling(
            llist_loop_lower[n_row][n_col]
            )
        
# 创建front面的线环和面
curve_loop_front = np.concatenate((llist_x_lower[0], 
                                   [llist_z_10], 
                                   [-llist_x_upper_0], 
                                   [-llist_z_00])).astype(int).tolist()
s_front = factory.addPlaneSurface([factory.addCurveLoop(curve_loop_front)])

# 创建back面的线环和面
curve_loop_back = np.concatenate((llist_x_lower[-1], 
                                  [llist_z_11], 
                                  [-llist_x_upper_1], 
                                  [-llist_z_01])).astype(int).tolist()
s_back = factory.addPlaneSurface([factory.addCurveLoop(curve_loop_back)])

# 创建left面的线环和面
curve_loop_left = np.concatenate((llist_y_lower[:, 0], 
                                  [llist_z_01], 
                                  [-llist_y_upper_0], 
                                  [-llist_z_00])).astype(int).tolist()
s_left = factory.addPlaneSurface([factory.addCurveLoop(curve_loop_left)])

# 创建right面的线环和面
curve_loop_right = np.concatenate((llist_y_lower[:, -1], 
                                   [llist_z_11], 
                                   [-llist_y_upper_1], 
                                   [-llist_z_10])).astype(int).tolist()
s_right = factory.addPlaneSurface([factory.addCurveLoop(curve_loop_right)])

# 创建top面的线环和面
curve_loop_top = np.array([llist_x_upper_0, 
                           llist_y_upper_1, 
                           -llist_x_upper_1, 
                           -llist_y_upper_0]).astype(int).tolist()
s_top = factory.addPlaneSurface([factory.addCurveLoop(curve_loop_top)])

# 创建体
surface_loop = np.concatenate((slist_lower.flatten(),
                [s_front, s_back, s_left, s_right, s_top])).astype(int).tolist()
v = factory.addVolume([factory.addSurfaceLoop(surface_loop)])

# 底面向下进行拉伸创建边界层网格
surface_to_extrude = [(2, s_index) for s_index in slist_lower.flatten()]
out_dim_tags = factory.extrude(
    surface_to_extrude,
    0, 0, -zLayer,  # extrusion along z-axis
    numElements=[1,1,1,1,1], 
    heights=[0.1343797033,0.2956353472,0.4891421200,0.7213502473,1], #todo: 编写边界层厚度计算程序
    recombine=True
)
extrude_v_list = [tag for tag in out_dim_tags if tag[0] == 3]

factory.synchronize()

# 提取所有的侧面
assert len(out_dim_tags) % 6 == 0 #todo: 侧面的个数应该是6的倍数（解释一下）
group_num = int(len(out_dim_tags)/6)
# 使用掩码获取拉出来的底面，侧面的tag序号
mask_side = [False,False,True,True,True,True] * group_num
mask_terrain = [True,False,False,False,False,False] * group_num
s_side = np.array(out_dim_tags)[mask_side]
s_new_terrain = np.array(out_dim_tags)[mask_terrain]
# 去重
s_side = np.unique(s_side,axis=1)

x_min_list =  []
x_max_list =  []
y_min_list =  []
y_max_list =  []
for s_tag in s_side:
    xmin, ymin, zmin, xmax, ymax, zmax = gmsh.model.getBoundingBox(s_tag[0], s_tag[1])
    x_min_list.append(xmin)
    x_max_list.append(xmax)
    y_min_list.append(ymin)
    y_max_list.append(ymax)
# 所有侧面的xy坐标最大最小值
x_min_all = np.min(x_min_list)
x_max_all = np.max(x_max_list)
y_min_all = np.min(y_min_list)
y_max_all = np.max(y_max_list)

# 筛选出总体的四个侧面
is_minx = x_min_list < (x_min_all + tol_x)
is_miny = y_min_list < (y_min_all + tol_y)
is_maxx = x_max_list > (x_max_all - tol_x)
is_maxy = y_max_list > (y_max_all - tol_y)
is_normal_to_x = (np.array(x_max_list) - np.array(x_min_list)) < tol_x
is_normal_to_y = (np.array(y_max_list) - np.array(y_min_list)) < tol_y

s_xmin_index = s_side[is_minx & is_normal_to_x][:,1]
s_xmax_index = s_side[is_maxx & is_normal_to_x][:,1]
s_ymin_index = s_side[is_miny & is_normal_to_y][:,1]
s_ymax_index = s_side[is_maxy & is_normal_to_y][:,1]

factory.synchronize()
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.model.addPhysicalGroup(2, s_new_terrain[:,1].tolist(), name="terrain")
gmsh.model.addPhysicalGroup(2, [s_front]+s_ymin_index.tolist(), name="front")
gmsh.model.addPhysicalGroup(2, [s_right]+s_xmax_index.tolist(), name="outlet")
gmsh.model.addPhysicalGroup(2, [s_back]+s_ymax_index.tolist(), name="back")
gmsh.model.addPhysicalGroup(2, [s_left]+s_xmin_index.tolist(), name="inlet")
gmsh.model.addPhysicalGroup(2, [s_top], name="upperWall")
gmsh.model.addPhysicalGroup(3, [v]+[tag[1] for tag in extrude_v_list], name="interfluid")
gmsh.model.mesh.generate(3)
# gmsh.model.mesh.optimize()
gmsh.write("mesh.msh")
gmsh.finalize()