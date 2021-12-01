from time import sleep


class Place:
    def __init__(self, tokens=0):
        self.tokens = tokens


class Preset:
    def __init__(self, place, transaction=1):
        self.place = place
        self.transaction = transaction

    def is_enabled(self):
        if self.place.tokens >= self.transaction:
            return True
        return False

    def tokens_out(self):
        self.place.tokens -= self.transaction


class Postset:
    def __init__(self, place, transaction=1):
        self.place = place
        self.transaction = transaction

    def tokens_in(self):
        self.place.tokens += self.transaction


class Transition:
    def __init__(self, input_places, output_places):
        self.input_places = input_places
        self.output_places = output_places

    def fire(self):
        count = 0
        allow_firing = False
        for place in self.input_places:
            if place.is_enabled():
                count += 1
        if count == len(self.input_places):
            allow_firing = True

        if allow_firing:
            for place in self.input_places:
                place.tokens_out()
            for place in self.output_places:
                place.tokens_in()

        return allow_firing


class PetriNet:
    def __init__(self, places, transitions):
        self.places = places
        self.transitions = transitions

    def get_places(self):
        print("State P = {", end="")
        for place in self.places:
            if place == self.places[-1]:
                for key in place.keys():
                    print(f"{key}", end='}\n')
                break
            for key in place.keys():
                print(f"{key}", end=', ')

    def get_transitions(self):
        transition_names = [name for name in self.transitions.keys()]
        print("Transition T = {", end="")
        for transition_name in transition_names:
            if transition_name == transition_names[-1]:
                print(transition_name, end='}\n')
                break
            print(transition_name, end=", ")

    def get_marking(self, t):
        if t == 'initial':
            print('Initial marking: [', end="")
        else:
            print(f'[{t}] fired')
            print('Marking: [', end="")
        for place in self.places:
            if place == self.places[-1]:
                for key, value in place.items():
                    print(f"{value.tokens}.{key}", end=']\n')
                break
            for key, value in place.items():
                print(f"{value.tokens}.{key}", end=', ')

    def auto_fire(self, trans):
        self.get_marking('initial')
        checking = True
        while checking:
            for transition_name in trans:
                full_of_tokens = True
                while full_of_tokens:
                    t = self.transitions[transition_name]
                    if t.fire():
                        self.get_marking(transition_name)
                        sleep(0.5)
                    else:
                        full_of_tokens = False
            count = 0
            for transition_name in trans:
                t = self.transitions[transition_name]
                if t.fire():
                    count += 1

            if count == 0:
                checking = False



def run_item1():
    print('Program is running...')
    ps = [{'free': Place(1)}, {'busy': Place(0)}, {'document': Place(0)}]
    ts = dict(start=Transition([Preset(ps[0]['free'])], [Postset(ps[1]['busy'])]),
              change=Transition([Preset(ps[1]['busy'])], [Postset(ps[2]['document'])]),
              end=Transition([Preset(ps[2]['document'])], [Postset(Preset(ps[0]['free']))])
              )

    pt = PetriNet(ps, ts)
    pt.get_places()
    pt.get_transitions()


def run_item2():
    print('Program is running...')
    wait_tokens = int(input('Wait: '))
    inside_tokens = int(input('Inside: '))
    done_tokens = int(input('Done: '))
    ps = [{'wait': Place(wait_tokens)},
          {'inside': Place(inside_tokens)},
          {'done': Place(done_tokens)}]
    ts = dict(start=Transition([Preset(ps[0]['wait'])], [Postset(ps[1]['inside'])]),
              change=Transition([Preset(ps[1]['inside'])], [Postset(ps[2]['done'])]),
              )
    pt = PetriNet(ps, ts)
    pt.auto_fire([name for name in ts.keys()])


def run_item3():
    print('Program is running...')
    wait_tokens = int(input('Wait: '))
    inside_tokens = int(input('Inside: '))
    done_tokens = int(input('Done: '))

    free_tokens = int(input('Free: '))
    busy_tokens = int(input('Busy: '))
    docu_tokens = int(input('Document: '))
    ps = [{'wait': Place(wait_tokens)},         # 0
          {'inside': Place(inside_tokens)},     # 1
          {'done': Place(done_tokens)},         # 2
          {'free': Place(free_tokens)},         # 3
          {'busy': Place(busy_tokens)},         # 4
          {'docu': Place(docu_tokens)},         # 5
          ]
    ts = dict(start=Transition([Preset(ps[0]['wait']), Preset(ps[3]['free'])], [Postset(ps[1]['inside']), Postset(ps[4]['busy'])]),
              change=Transition([Preset(ps[1]['inside']), Preset(ps[4]['busy'])], [Postset(ps[2]['done']), Postset(ps[5]['docu'])]),
              end=Transition([Preset(ps[5]['docu'])], [Postset(ps[3]['free'])])
              )
    pt = PetriNet(ps, ts)
    pt.auto_fire([name for name in ts.keys()])

def run_item4():
    print('Program is running...')
    wait_tokens = 3
    inside_tokens = 0
    done_tokens = 1

    free_tokens = 1
    busy_tokens = 0
    docu_tokens = 0
    ps = [{'wait': Place(wait_tokens)},  # 0
          {'inside': Place(inside_tokens)},  # 1
          {'done': Place(done_tokens)},  # 2
          {'free': Place(free_tokens)},  # 3
          {'busy': Place(busy_tokens)},  # 4
          {'docu': Place(docu_tokens)},  # 5
          ]
    ts = dict(start=Transition([Preset(ps[0]['wait']), Preset(ps[3]['free'])],
                               [Postset(ps[1]['inside']), Postset(ps[4]['busy'])]),
              change=Transition([Preset(ps[1]['inside']), Preset(ps[4]['busy'])],
                                [Postset(ps[2]['done']), Postset(ps[5]['docu'])]),
              end=Transition([Preset(ps[5]['docu'])], [Postset(ps[3]['free'])])
              )
    pt = PetriNet(ps, ts)
    pt.auto_fire([name for name in ts.keys()])

if __name__ == '__main__':
    c = True
    while c:
        item = int(input('Choose the item(1, 2, 3 or 4): '))
        if item == 1:
            run_item1()
        elif item == 2:
            run_item2()
        elif item == 3:
            run_item3()
        else:
            run_item4()
        user_input = True
        while user_input:
            q = input('Press Q to quit    |    Press R to continue\n Your choice: ')
            if q == 'Q':
                user_input, c = False, False
            elif q == 'R':
                user_input, c = False, True
            elif q != 'R':
                print('Baka onii-chan! (͡° ͜ʖ ͡°)')


