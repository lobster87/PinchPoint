class stream:
    def __init__(self, stream_number, inletT, outletT, CP):
        self.stream_number = stream_number
        self.inletT = inletT
        self.outletT = outletT
        self.CP = CP
        self.classification = None  # identify if hot or cold stream

        self.intervalTinlet = None
        self.intervalToutlet = None

    def intervalT(self, dtmin):
        # Calculate the interval temperatures for the streams
        # Hot stream
        if self.inletT > self.outletT:
            self.intervalTinlet = self.inletT - (dtmin / 2)
            self.intervalToutlet = self.outletT - (dtmin / 2)
            self.classification = 'Hot'

        # Cold stream
        else:
            self.intervalTinlet = self.inletT + (dtmin / 2)
            self.intervalToutlet = self.outletT + (dtmin / 2)
            self.classification = 'Cold'

    def inInterval(self, Tupper, Tlower, row, column, matrix):
        # Finds if streams is in the interval

        # for hot streams
        if self.classification == 'Hot':
            if self.intervalTinlet >= Tupper and self.intervalToutlet <= Tlower:
                matrix[row, column] = 1

        # Cold streams
        else:
            if self.intervalTinlet <= Tlower and self.intervalToutlet >= Tupper:
                matrix[row, column] = 1

