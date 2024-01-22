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
        return 100 * (arg2 * (arg5 - arg4) / (arg7 - arg6)) * ((arg3 * pow(arg7, 2) * exp(-arg1 / (arg3 * arg4)) / ( arg1 + 2 * arg3 * arg4 )) - (arg3 * pow(arg6, 2) * exp(-arg1 / (arg3 * arg6)) / ( arg1 + 2 * arg3 * arg6 )));
    }
} // namespace HCTTIEXP

