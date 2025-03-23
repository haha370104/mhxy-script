import random


def simulate_equipment(gems_per_equip):
    """
    模拟单件装备的洗练过程
    :param gems_per_equip: 每件装备初始打的宝石数量
    :return: True（达标）或 False（损毁）
    """
    current = gems_per_equip * 10  # 初始属性值
    while True:
        if current >= 100000:  # 达标条件
            return True
        if current < 5:  # 损毁条件
            return False

        # 洗练操作
        if random.random() < 0.5:
            # 50%概率：属性减半（向下取整）
            current = current * 0.42
        else:
            # 50%概率：属性乘以1.3~2.3的随机倍数
            current *= random.uniform(1.3, 2.2)


def run_simulation(player_gems, batch_size, gems_per_equip):
    """
    单次完整模拟：尝试用有限的宝石生成达标装备
    :return: 是否在宝石耗尽前成功
    """
    remaining_gems = player_gems
    while remaining_gems >= batch_size * gems_per_equip:
        # 扣除本批次的宝石
        remaining_gems -= batch_size * gems_per_equip

        # 模拟本批次所有装备
        for _ in range(batch_size):
            if simulate_equipment(gems_per_equip):
                return True  # 本批次有装备达标

    return False  # 所有批次均失败


def calculate_success_rate(player_gems, batch_size, gems_per_equip, sim_times=10000):
    """
    计算成功率
    :param sim_times: 模拟次数
    :return: 成功率（胜利次数 / 模拟次数）
    """
    victories = 0
    for _ in range(sim_times):
        if run_simulation(player_gems, batch_size, gems_per_equip):
            victories += 1
    return victories / sim_times


# ------------------- 示例调用 -------------------
if __name__ == "__main__":
    # 参数设置（可修改）
    player_gems = 3000  # 玩家当前宝石总量
    batch_size = 4  # 每批次装备数量
    gems_per_equip = 15  # 每件装备初始宝石数
    sim_times = 10000  # 模拟次数

    # 计算并打印成功率
    success_rate = calculate_success_rate(
        player_gems, batch_size, gems_per_equip, sim_times
    )
    print(f"成功率: {success_rate:.2%}")