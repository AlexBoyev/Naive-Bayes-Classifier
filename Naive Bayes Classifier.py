from Tkinter import *
import tkFileDialog

import ttk
import tkMessageBox
import csv
import os
import math

attributes = []
filename = ""
train_list = []
temp = []
test_class = []
progress = 0
accuracy = float(0.0)
k = 0

class NaiveBayes:
    total = 0
    """Naive Bayes classifier class with performing and helping functions"""

    def is_empty(self, file):
        """verify that the file is not empty"""
        if os.stat(file).st_size == 0:
            return True
        return False

    def read_file_to_list(self, path_name):
       """Stores the entered directory for the needed files"""
       global filename
       filename = tkFileDialog.askdirectory(title = "Select files")

    def build(self):
        """Reads in the file with the data"""
        global train_list
        global temp
        global attributes
        global filename
        global progress
        global accuracy

        try:
            def read_structure():
                """Reads in structure for the file with the data"""

                attributes = []
                try:
                    if self.is_empty(filename + "/Structure.txt"):
                        tkMessageBox.showinfo("Error", "Structure.txt file is empty")
                        raise Exception
                    with open(filename + "/Structure.txt", "r") as structure_file:
                        content = structure_file.readlines()
                    content = [x.strip() for x in content]
                    for x in content:
                        x_spl = x.split(' ')
                        if x_spl[0] == "@ATTRIBUTE":
                            if x_spl[2] == "NUMERIC":
                                attributes.append(x_spl[2])
                            else:
                                x_spl_list = x_spl[2][1:len(x_spl[2]) - 1].split(',')
                                attributes.append(x_spl_list)

                    return attributes # attirbutes is a a list of categories of classifed model
                except:
                    tkMessageBox.showinfo("Error", "Error opening Structure.txt")
                    raise

            attributes = read_structure()

            try:
                with open(filename + "/train.csv", 'rb') as f:
                    reader = csv.reader(f)
                    if self.is_empty(filename + "/train.csv"):
                        tkMessageBox.showinfo("Error", "train.csv file is empty")
                        return
                    temp = list(reader)
                    train_list = []
                    for i in range(1, len(temp)):# changed 0-> 1 + if i != 0:
                            train_list.append(temp[i])



            except:
                tkMessageBox.showinfo("Error", "Error opening train.csv")
                return

            tkMessageBox.showwarning("Building ended", "Building classifier using train-set is done!", icon="info")
        except:
            tkMessageBox.showwarning("Building failed", "Building failed", icon="info")
            # return

    def classify(self, bins, mylabel2,mylabel3):
        """Performs the classification of the file data using Naive Bayes algorithm"""
        mylabel2.set("Proccessing...")
        window.update()

        global train_list
        global temp
        global attributes
        global filename
        global test_class
        global k

        try:
            bins = int(bins.get())
        except:
            tkMessageBox.showinfo("Error", "Wrong entrance for bins")
            mylabel2.set("")
            return

        if bins < 0:
            tkMessageBox.showinfo("Error", "Wrong entrance for bins")
            mylabel2.set("")
            return

        try:
            with open(filename + "/test.csv", 'rb') as f: # filename_test
                reader = csv.reader(f)
                if self.is_empty(filename + "/test.csv"):
                    tkMessageBox.showinfo("Error", "test.csv file is empty")
                    mylabel2.set("")
                    return
                temp = list(reader)
                test_list = []
                for i in range(1, len(temp)): #making list from test file without the categories
                        test_list.append(temp[i])

                for raw in test_list: #making a list of answers yes/no to check accuracy
                    test_class.append(raw[-1])
        except:
            tkMessageBox.showinfo("Error", "Error opening test.csv")
            mylabel2.set("")
            return

        def fill_empty(list, attributes):
           """Fills in the empty places in the data list"""
           for i in range(0, len(attributes)):
               if attributes[i] == 'NUMERIC':
                   for j in range(0, len(list)):
                       if list[j][i] == '':
                           list[j][i] = get_average(train_list, i)
               else:
                   for j in range(0, len(list)):
                       if list[j][i] == '':
                           list[j][i] = get_common(train_list, i, attributes)
           return list

        def get_average(list, num):

            """Computes the average for the file data"""
            sum = 0
            amount = 0
            for i in range(0, len(list)):
                if list[i][num] != '':
                    sum += list[i][num]
                    amount += 1
            return sum / amount

        def get_common(list, num, attributes):
            """Computes the most appeared value for the file data"""
            attributes_amounts = [] # a list with the amounts of values
            i = 0
            for elem in attributes[num]:
                attributes_amounts.append(0)
                for j in range(0, len(list)):
                    if list[j][num] == elem:
                        attributes_amounts[i] += 1
                i += 1
            max = attributes_amounts[0]
            mostappeared_attr = attributes[num][0]

            for i in range(0, len(attributes_amounts)):
                if max < attributes_amounts[i]:
                    max = attributes_amounts[i]
                    mostappeared_attr = attributes[num][i]
            return mostappeared_attr

        def to_numeric(list, num):
            """Transforms the data list where it is numeric to the numeric python values"""
            for i in range(0, len(list)):
                if list[i][num] != '':
                    list[i][num] = float(list[i][num])
            return list

        def discretize(train_list, num, bins_num):
            """Discretizes the columns with continuous values"""
            if bins_num <= 0:
                mylabel2.set("")
                raise Exception
            min = min_in_column(train_list, num)
            max = max_in_column(train_list, num)
            bins_width = int(math.ceil(float(max - min) / bins_num)) # round the bins up

            binarray = range(int(min), int(max), bins_width)

            if len(binarray) != 0:   #fix the binarray index error
                binarray.append(binarray[-1] + bins_width)

            for raw in train_list:
                for index in range(0,len(binarray)):
                    if raw[num] <= binarray[index]:
                        raw[num] = index + 1
                        break #stops the set in correct interval

            return train_list

        def min_in_column(list, num):
            """Finds the minimum number in the column"""
            min = list[0][num]
            for elem in list:
                if elem[num] < min:
                    min = elem[num]
            return min

        def max_in_column(list, num):
            """Finds the maximum number in the column"""
            max = list[0][num]
            for elem in list:
                if elem[num] > max:
                    max = elem[num]
            return max

        def total_class(list,class_val,attributes):
            "Calculates the total frequency of the given class value"
            class_val_count = 0.0

            for i in range(0, len(list)):
                if list[i][len(attributes) - 1] == class_val:
                    class_val_count += 1
            if class_val_count == 0.0:
                class_val_count += 1
            return class_val_count/len(list)

        def cond_prob(list, column, specific_elem, class_val, attributes):
            """Computes the conditional probability for some item depending on class value"""
            count = 0.0
            class_val_count = 0.0

            for i in range(0, len(list)):
                if list[i][column] == specific_elem and list[i][len(attributes) - 1] == class_val:
                    count += 1
                if list[i][len(attributes) - 1] == class_val:
                    class_val_count += 1
            if class_val_count == 0.0:
                class_val_count += 1
            if count == 0.0:
                count += 1
            return count/class_val_count

        for i in range(0, len(attributes)):
            if attributes[i] == 'NUMERIC':
                train_list = to_numeric(train_list, i)
                test_list = to_numeric(test_list, i)

        train_list = fill_empty(train_list, attributes)
        test_list = fill_empty(test_list, attributes)

        for i in range(0, len(attributes)):
            if attributes[i] == 'NUMERIC':
                train_list = discretize(train_list, i, bins)
                test_list = discretize(test_list, i, bins)

        def bayes(list, attributes):
            """Performs Bayes classification with Laplacian fix using its formula"""
            total = len(test_list)
            progress = 0
            our_class = []
            global k

            mylabel3.set("progress: {}/{}.".format(progress, total))
            window.update()

            output = open(filename+'/output.txt', 'w')

            class_list = attributes[-1]

            for elem in test_list:

                for j in range(1, len(class_list)):

                    propability = 1

                    true_propability = 1

                    true_classifier = class_list[0]

                    for i in range(0, len(attributes)-1):
                        true_propability *= cond_prob(list, i, elem[i], class_list[0], attributes)
                    true_propability *= total_class(list, class_list[0], attributes)

                    for i in range(0, len(attributes)-1):
                        propability *= cond_prob(list, i, elem[i], class_list[j], attributes)
                    propability *= total_class(list, class_list[j], attributes)

                    if propability > true_propability:
                        true_classifier = class_list[j]
                k += 1
                output.write(str(k))
                output.write('\n\n')
                progress += 1
                our_class.append(true_classifier)
                mylabel3.set("progress: {}/{}.".format(progress, total))
                window.update()
                output.write(true_classifier)
                output.write('\n\n')

                #if j == 5:
                   #break

            output.close()
            n = sum(i == j for i, j in zip(our_class, test_class))
            accuracy = float(float(n)/float(len(test_class)))

            tkMessageBox.showwarning("Classification ended", "The classification has been performed. the accuracy is: {0:.4f}%.".format( float(accuracy * 100)), icon="info")

        bayes(train_list, attributes)

        mylabel2.set("")


        exit()

window = Tk()

window.geometry("800x400")
window.resizable(0, 0)
window.title("Naive Bayes classifier")

path = StringVar()
pathEntered = ttk.Entry(window, width = 70, textvariable = path)
pathEntered.place(x=205, y=150, width=400)

mylabel = Label(window, text="Directory Path")
mylabel.place(x=80, y=150, height=20, width=95)

binsEntered = StringVar()
bins = ttk.Entry(window, width = 40, textvariable = binsEntered)
bins.place(x=205, y=190,width=400)

mylabel1 = Label(window, text="Discretization Bins")
mylabel1.place(x=80, y=190, height=20, width=122)

mylabel2 = Label(window) # Proccessing... # textvariable = label2Text
mylabel2.place(x=350, y=670, height=20, width=100)
label2Text = StringVar()
mylabel2.configure(textvariable=label2Text)
mylabel2.pack()

mylabel3 = Label(window) # Proccessing... # textvariable=label2Text
mylabel3.place(x=350, y=550, height=20,width=100)
label3Text = StringVar()
mylabel3.configure(textvariable=label3Text)
mylabel3.pack()

nb = NaiveBayes()

B = Button(window, text = "Browse")
B.place(x = 620, y = 145, width = 100, height = 30)
B.bind("<ButtonPress-1>", lambda event, arg = pathEntered: nb.read_file_to_list(arg))

B = Button(window, text = "Build") # , command = build
B.place(x = 350, y = 240, width = 150, height = 25)
B.bind("<ButtonPress-1>", lambda event: nb.build()) # command = build()

B = Button(window, text = "Classify") # , command = classify
B.place(x = 350, y = 270, width = 150, height = 25)
B.bind("<ButtonPress-1>", lambda event, arg=bins, arg1=label2Text,arg2=label3Text: nb.classify(arg, arg1,arg2)) # command = classify()) #

window.mainloop()

