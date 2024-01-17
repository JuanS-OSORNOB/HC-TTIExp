#ifndef TTI_H
#define TTI_H
class TTI
{
    public:
        TTI();
        ~TTI();
    
        /**
         * @brief 
         * This function computes the TTI Arr
         * @param arg1 E: Activation energy (kJ/mol).
         * @param arg2 A: Pre-exponential or frequency factor (1/m.y.).
         * @param arg3 R: Ideal gas constant (J/K*mol).
         * @param arg4 t: Final geological time of exposition.
         * @param arg5 tf: Initial geological time of exposition
         * @param arg6 T: Final absolute temperature (K = °C+273) at the end of the exposure time
         * @param arg7 K: Initial absolute temperature (K = °C+273) at the beginning of the exposure time 
         * @return double 
         */
        double ttiarr(double arg1, double arg2, double arg3, double arg4, double arg5, double arg6, double arg7);
    
    private:
};
#endif