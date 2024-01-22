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
        return 100 * (arg1 * (arg2 - arg3)/(arg4 - arg5)) * (((arg6 * pow(arg4, 2) * exp(-arg7 / (arg6 * arg4)))/(arg7 + 2 * arg6 * arg4)) - ((arg6 * pow(arg5, 2) * exp(-arg7 / (arg6 * arg5)))/(arg7 + 2 * arg6 * arg5)));
    }
} // namespace HCTTIEXP

