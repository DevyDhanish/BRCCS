from lib.ReadnWrite.RnW import ReaderAndWriter

data = {
    "done" : "Done"
}

if __name__ == "__main__":
    rnw = ReaderAndWriter()
    print(rnw.read_file("test.json"))
    rnw.write_to_file("out.json", data)