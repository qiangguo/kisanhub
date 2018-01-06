from data_collection import data_request
import numpy

class Regression:
    """
    This class defines regression model. It proposes the
    implementations of linear regression and locally weighted
    linear regression
    """
    def __init__(self, k=1.0):
        self.kernel_k = k


    def get_data(self):
        A, B = data_request.get_annual_regression_data('max_temp', 'min_temp')
        if A==[] or B==[]:
            return ('ERROR', 'No data is populated in the database')
        else:
            return ('OK', (A, B))


    def kernel_function(self, Mat):
        """ Define kernel function used for locally weighted
            linear regression. """
        return numpy.exp(Mat*Mat.T/(-2.0*self.kernel_k**2))


    def standRegres(self, xArr, yArr):
        """ Standard linear regression algorithm """
        xMat = numpy.mat(xArr)
        yMat = numpy.mat(yArr).T
        xTx = xMat.T * xMat
        if numpy.linalg.det(xTx) == 0.0:
            return ('ERROR', 'Matrix is singular, cannot do inverse')
        ws = xTx.I * (xMat.T * yMat)
        return ws


    def lwlr(self, localPoint, xArr, yArr):
        """ Locally weighted linear regression algorithm """
        xMat = numpy.mat(xArr)
        yMat = numpy.mat(yArr).T
        m = numpy.shape(xMat)[0]
        weights = numpy.mat(numpy.eye((m)))
        for j in range(m):
            diffMat = localPoint - xMat[j, :]
            weights[j,j] = self.kernel_function(diffMat)
        xTx = xMat.T * (weights * xMat)
        if numpy.linalg.det(xTx) == 0.0:
            return ('ERROR', "Mtrix is singular, cannot do inverse")
        ws = xTx.I * (xMat.T * (weights * yMat))
        return localPoint * ws
