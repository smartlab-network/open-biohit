from biohit_pipettor.pipettor import Pipettor


def run():
    with Pipettor() as inst:
        inst.initialize()
        print(inst.x_position, inst.y_position, inst.z_position)
        inst.move_z(10)
        inst.move_xy(30, 30)
        inst.move_z(0)
        inst.move_xy(0, 0)
        print(inst.x_position, inst.y_position, inst.z_position)


run()
