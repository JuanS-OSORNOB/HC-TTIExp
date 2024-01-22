#ifndef TTI_H
#define TTI_H
namespace HCTTIEXP
{
    class TTI
    {
        public:
            /**
             * @brief 
             * This function computes the TTI Arr
             * @param arg1 A: Pre-exponential or frequency factor (1/m.y.).
             * @param arg2 Y: Final geological time of exposition (tn+1).
             * @param arg3 X: Initial geological time of exposition (tn).
             * @param arg4 K: Final absolute temperature (K = °C+273) at the end of the exposure time (Tn+1).
             * @param arg5 T: Initial absolute temperature (K = °C+273) at the beginning of the exposure time (Tn).
             * @param arg6 R: Ideal gas constant (J/K*mol).
             * @param arg7 E: Activation energy (kJ/mol).
             * @return double 
             */
            double ttiarr(double arg1, double arg2, double arg3, double arg4, double arg5, double arg6, double arg7);

        private:
    };
} // namespace HCTTIEXP

#endif