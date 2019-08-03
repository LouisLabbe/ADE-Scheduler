import itertools as itools

class Computation:
    """
    Class defining the computation of a scheduling.
    For the moment, computed to work for a one-week schedule
    => Class not necessary, but for the moment, it is simpler to do so
    """

    def __init__(self):
        self.courses = []
        self.up_to_date = False
        self.valid = []

    def add_course(self, course):
        if not course in self.courses:
            self.courses.append(course)
        up_to_date = False
    
    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
        up_to_date = False
    
    def add_valid_schedule(self, schedule):
        """
        Add the valid schedule in valid as a form of dictionnary
        @pre: schedule is a valid schedule
        @post: -
        """
        new_valid = {}
        for i, course in enumerate(self.courses):
            self.valid[course.code] = schedule[i]
        self.valid.append(new_valid)

    def compute(self):
        """
        Computes all the valids schedulings for the given courses
        in self.courses, where each course has his own slots
        ---------------------------------------------------------
        A 'valid' scheduling is one which has no conflict for all
        the courses (CM/APE).
        TO DO: preferences

        @post: a list of dictionnaries, where each item is a 
        valid schedule. Each dictionnary has the form code:slot :
        - code is the code of the course (e.g. 'LINMA1510')
        - slot is the slot object (of class Slot)

        /!\ The dictionnary is only computed if there is a change
            since the last computation
        """
        
        # No change since last time
        if self.up_to_date:
            return self.valid
        
        # Reset the valid, since changes
        self.valid = []

        all_slots = []
        for c in self.courses:
            all_slots.append(c.slots)
        
        # Computing the permutations based on the slots
        permutations = list(itools.product(*all_slots))

        # Looping through permutations
        for perm in permutations:
            # Looping through the slots of perm, checking if valid
            overlap = False # Stop the loop if there is an overlap

            """
            This method can be improved !
            Idea: cheking thanks to Python build-in methods if there exists any two
            copies of a slot in the list
            Requires: permute the definition of Slot.__eq__ and Slot.overlap
            /!\ Doing so will break the methods: Cours.add_slot and Cours.remove_slot
                because it uses the actual __eq__ method to check if two slot are identical
                to avoid duplicates in the list
            """
            for i in range(len(perm)-1):
                if overlap:
                    break
                for j in range(1, len(perm)):
                    if i.overlap(j):
                        overlap = True
                        break
            # No overlap: it is a valid schedule
            if not overlap:
                add_valid_schedule(perm)
        
        self.up_to_date = True
        return self.valid
