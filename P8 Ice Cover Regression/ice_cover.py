'''
Evan Hansen
CS 540
P8: Ice Cover Regression
'''

if __name__=="__main__":

    import random

    # Returns dataset in n x 2 array
    def get_dataset():
        dataset = []
        f = open('ice.txt','r')
        for l in f:
            xy_pair = l.split()
            xy_pair = [int(i) for i in xy_pair]
            dataset.append(xy_pair)
        return dataset


    dataset = get_dataset()


    def print_stats(dataset):

        n = len(dataset)
        y_bar = 0
        for d in dataset:
            y_bar += d[1]/n

        sd = 0
        for d in dataset:
            sd += (d[1]-y_bar)**2/(n-1)

        sd = sd**(1/2)

        # Number of data points
        # Sample mean
        # Sample Standard Deviation
        print(n)
        print(round(y_bar, 2))
        print(round(sd, 2))
        return


    def regression(beta_0, beta_1, ds=dataset):
        MSE = 0
        for d in ds:
            MSE += (beta_0 + beta_1*d[0] - d[1])**2 / len(ds)

        return MSE


    def gradient_descent(beta_0, beta_1, ds=dataset):
        n = len(ds)
        db0 = 0
        db1 = 0

        for d in ds:
            db0 += (2/n) * (beta_0 + beta_1*d[0] - d[1])
            db1 += (2 / n) * (beta_0 + beta_1 * d[0] - d[1]) * d[0]

        return db0, db1


    def iterate_gradient(T, eta, ds=dataset):
        b0 = 0
        b1 = 0
        for i in range(T):
            grad = gradient_descent(b0, b1, ds)
            b0 = b0 - eta*grad[0]
            b1 = b1 - eta*grad[1]
            MSE = regression(b0, b1)
            print(i+1, round(b0, 2), round(b1, 2), round(MSE, 2))


    def compute_betas():
        ds = dataset
        n = len(ds)
        y_bar = 0
        x_bar = 0

        for d in ds:
            y_bar += d[1] / n
            x_bar += d[0] / n

        s_top = 0
        s_bot = 0
        for d in ds:
            s_top += (d[0] - x_bar)*(d[1] - y_bar)
            s_bot += (d[0] - x_bar)**2
        b1 = s_top/s_bot
        b0 = y_bar - b1*x_bar
        MSE = regression(b0, b1)

        return b0, b1, MSE


    def predict(year):
        betas = compute_betas()
        y_hat = betas[0] + betas[1]*year
        return y_hat


    def iterate_normalized(T, eta):
        ds = dataset
        norm_ds = ds[:]
        n = len(ds)

        x_bar = 0
        for d in ds:
            x_bar += d[0] / n

        sdx = 0
        for d in ds:
            sdx += (d[0] - x_bar) ** 2 / (n - 1)
        sdx = sdx ** (1 / 2)

        for xy in norm_ds:
            xy[0] = (xy[0] - x_bar)/sdx

        iterate_gradient(T, eta, norm_ds)


    def sgd(T, eta):
        ds = dataset
        norm_ds = ds[:]
        n = len(ds)

        x_bar = 0
        for d in ds:
            x_bar += d[0] / n

        sdx = 0
        for d in ds:
            sdx += (d[0] - x_bar) ** 2 / (n - 1)
        sdx = sdx ** (1 / 2)

        for xy in norm_ds:
            xy[0] = (xy[0] - x_bar) / sdx

        # Gradient Iteration
        b0 = 0
        b1 = 0
        for i in range(T):
            rand_xy = random.choice(norm_ds)
            xjt = rand_xy[0]
            yjt = rand_xy[1]

            db0 = 2 * (b0 + b1 * xjt - yjt)
            db1 = 2 * (b0 + b1 * xjt - yjt) * xjt

            b0 = b0 - eta * db0
            b1 = b1 - eta * db1
            MSE = regression(b0, b1)
            print(i + 1, round(b0, 2), round(b1, 2), round(MSE, 2))


