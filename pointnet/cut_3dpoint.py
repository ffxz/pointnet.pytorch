import laspy

class CutLas:
    def __init__(self):
        pass
    

    def read_las(self, lasfile):
        las_ori = laspy.read(lasfile)
        header = laspy.LasHeader(point_format=las_ori.header.point_format, version=las_ori.header.version)
        header.add_extra_dim(laspy.ExtraBytesParams(name="height_classes", type=np.int32))
        output_file = laspy.LasData(header)
        # x_array = np.array(las_ori.x)
        # y_array = np.array(las_ori.y)
        # z_array = np.array(las_ori.z)
    return las_ori.xyz #x_array, y_array, z_array

    def voxel_filter(self, point_cloud, leaf_size, mode):
        '''

        Args:
            point_cloud:
            leaf_size:
            mode:
            # 实现voxel滤波，并加载数据集中的文件进行验证
            # 功能：对点云进行voxel滤波
            # 输入：
            #     point_cloud：输入点云
            #     leaf_size: voxel尺寸

        Returns:

        '''
        filtered_points = []
        data = point_cloud
        # 作业3
        # 屏蔽开始
        # 1.计算点云的最大最小值
        D_min = data.min(0)
        D_max = data.max(0)
        # 2.设定划分体素大小，计算空间划分份数1ｘ3
        D = (D_max - D_min) / leaf_size
        # 3.每个点计算划分索引
        point_x, point_y, point_z = np.array(data.x), np.array(data.y), np.array(data.z)
        hx = np.floor((point_x - D[0]) / leaf_size)
        hy = np.floor((point_y - D[1]) / leaf_size)
        hz = np.floor((point_z - D[2]) / leaf_size)
        index = np.array(np.floor(hx + hy * D[0] + hz * D[0] * D[1]))  # Nｘ1

        # 不进行排序，使用哈希映射进行点的筛选#

        # 4.对索引进行排序
        data_index_point = np.c_[index, point_x, point_y, point_z]
        sort_idx = data_index_point[:, 0].argsort()
        data_index_point = data_index_point[sort_idx]
        size = data_index_point.shape[0]
        tem_point = []
        if mode == 1:
            # 使用随机采样方法,索引相同的点选取最后一个为滤波输出点，相当于是随机采样了
            for i in range(size - 1):
                if (data_index_point[i][0] != data_index_point[i + 1][0]):
                    filtered_points.append(data_index_point[i][1:])
            # 最后一个没有比较，加上
            filtered_points.append(data_index_point[size - 1][1:])
            filtered_points = np.array(filtered_points)
        if mode == 2:
            # 使用计算均值方法
            for i in range(size - 1):
                # 判断前一个序号和后一个是否相等
                if data_index_point[i][0] == data_index_point[i + 1][0]:  # 对于只有两个点的就会只保留一个点
                    tem_point.append(data_index_point[i][1:])
                    continue
                if tem_point == []:
                    continue
                filtered_points.append(np.mean(tem_point, axis=0))
                tem_point = []
            filtered_points = np.array(filtered_points)

        # 4.利用哈希表将点的索引映射到哈希容器中，注意排除冲突的点

        # 屏蔽结束

        # 把点云格式改成array，并对外返回
        filtered_points = np.array(filtered_points, dtype=np.float64)
        return filtered_points


     



if __name__ == '__main__':
    a = CutLas()
    xyz = a.read_las('/data/libin/part15/hough_2timesv57.las')
    leaf_size = 10
    mode = 1
    voxel_filter(xyz, leaf_size, mode)


