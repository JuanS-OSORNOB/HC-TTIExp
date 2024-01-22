#include <HCTTIExpProjConfig.h>
#include <thermal_effects/tti.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

namespace HCTTIEXP
{    
    double TTI::ttiarr(double arg1, double arg2, double arg3, double arg4, double arg5, double arg6, double arg7)
    {
        double A = arg1;
        double Y = arg2;
        double X = arg3;
        double K = arg4 + 273;// Absolute temperature
        double T = arg5 + 273;// Absolute temperature
        double R = arg6;
        double E = arg7 * 1000;// 1 kJ = 1000 J
        
        double coefficient =  A * (Y - X) / (K - T);
        double first_term = R * pow(K, 2) * exp(-E/(R * K)) / (E + 2 * R * K);
        double second_term = R * pow(T, 2) * exp(-E/(R * T))/ (E + 2 * R * T);
        double TTI = 100 * coefficient * (first_term - second_term);
        return TTI;
    }
} // namespace HCTTIEXP

