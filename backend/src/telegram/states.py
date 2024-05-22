from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    phone = State()

    confirm_pickup = State()
    overweight_state = State()

    trauma_state = State()
    cholesterol_state = State()
    hearth_state = State()
    lactose_state = State()

    skin = State()
    fatigue = State()
    immunity = State()
    pain = State()