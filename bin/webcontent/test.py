import sched

turn = 1
exit_game = False


def get_turn(): 
    return turn

def advance_turns(num_turns):
    #advance N turns.
    global turn
    for i in range(num_turns):
        print 'Turn:', turn
        #this is where you'd check player input, draw the screen and stuff.
        turn += 1

def test_event(str):
    print 'Test event', str

def exit_event():
#cancel all events and exit the main loop.
    global exit_game
    exit_game = True
    for event in events.queue:
        events.cancel(event)


#initialize the scheduler with 2 test events and one exit event.
events = sched.scheduler(get_turn, advance_turns)
events.enter(11, 6, test_event, 'A')
events.enter(5, 1, test_event, 'B')
events.enter(20, 1, exit_event, ())

#main loop: run scheduler, or advance one turn if there are no events.
while not exit_game:
    if not events.empty():
        events.run()
    else:
        game_logic(1)