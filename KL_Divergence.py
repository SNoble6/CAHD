from math import log10 as log


class KL_Divergence:
    r = None

    def compute_Act(self, s, c):
        # numero occorrenze di s in C (solo quelle boh)
        # numero occorrenze di s nel dataset (copi histogram prima di modificarlo?)
        pass

    def compute_Est(self, s, c):
        pass

    #devo farla per ogni s, occhio che in un gruppo posso avere piu di una s
    def compute_kl_divergence(self, ):
        result = 0
        s = 0
        for c in r_QID:
            act = self.compute_Act(c, s)
            est = self.compute_Est(c, s)
            if act != 0 and est != 0:
                result += act * log(act / est)
        pass
