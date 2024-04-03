class Score():
    def __init__(self):
        """
        construct a class for score
        """
        # file_name = "score.txt"
        self.score_dict = {}
        self.sorted_dict = []

    def build_dict(self):
        """
        read existing file
        add data to a dictionary
        """
        with open("score.txt", "r") as f:
            for line in f:
                content = line.split()
                if len(content) != 0:
                    name = content[0]
                    score = int(content[1])
                    #  need to modify
                    if name in self.score_dict.keys():
                        self.score_dict[name] += score
                    else:
                        self.score_dict[name] = score

        f.close()

    def add_player(self, pl_name, pl_score):
        """
        add new player to the dictionary
        """
        if pl_name in self.score_dict.keys():
            self.score_dict[pl_name] += pl_score
        else:
            self.score_dict[pl_name] = pl_score

    def sort_the_data(self):
        """
        sort the data by value, from highest to lowest
        """
        self.sorted_dict = sorted(self.score_dict.items(),
                                  key=lambda x: x[1],
                                  reverse=True)

    def write_data(self):
        """
        write updated data to the txt file
        """
        f = open("score.txt", "w")

        for element in self.sorted_dict:
            wri_name = str(element[0])
            wri_score = str(element[1])
            f.write(wri_name + " " + wri_score + "\n")
        f.close()
