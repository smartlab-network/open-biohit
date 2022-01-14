from biohit_pipettor.pipettor import Pipettor


def run():
    with Pipettor() as inst:
        print(inst.is_connected)


run()
