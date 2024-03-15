import pickle

# TODO With this class, we want to save JSON data from Google Calendar, Weather API and Todo, to pickle
# We want to retrieve that data when the ap runs, and compare with what we have returned
# This will decide if we need to refresh the Inky screen or not.
# If the data is the same, there is no point in refreshing the screen.


def main():
    # data = {"DogName":"Frank","DogType":"Boston"}
    # pickle.dump(data, open( "save.p", "wb" ) )

    loadedData = pickle.load(open("./state/save.p", "rb"))
    print(loadedData["DogName"])


def save_todo_data(todojson):
    pickle.dump(todojson, open("./state/todo.p", "wb"))


if __name__ == "__main__":
    main()
