# Auto-generated from SysML v2 model (OttoEngine)
# Run this in Fusion 360 Scripts and Add-Ins

import adsk.core
import adsk.fusion

def run(context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        app.userInterface.messageBox('No active design')
        return

    userParams = design.userParameters
    updates = []

    # mass -> total_mass
    param = userParams.itemByName('total_mass')
    if param:
        param.expression = "18 kg"
        updates.append('total_mass')
    else:
        valueInput = adsk.core.ValueInput.createByString("18 kg")
        userParams.add('total_mass', valueInput, 'kg', 'From SysML: mass')
        updates.append('total_mass (created)')

    # ratedPower -> rated_power
    param = userParams.itemByName('rated_power')
    if param:
        param.expression = "110 kW"
        updates.append('rated_power')
    else:
        valueInput = adsk.core.ValueInput.createByString("110 kW")
        userParams.add('rated_power', valueInput, 'kW', 'From SysML: ratedPower')
        updates.append('rated_power (created)')

    # maxTorque -> max_torque
    param = userParams.itemByName('max_torque')
    if param:
        param.expression = "200 N*m"
        updates.append('max_torque')
    else:
        valueInput = adsk.core.ValueInput.createByString("200 N*m")
        userParams.add('max_torque', valueInput, 'N*m', 'From SysML: maxTorque')
        updates.append('max_torque (created)')

    # numberOfCylinders -> cylinder_count
    param = userParams.itemByName('cylinder_count')
    if param:
        param.expression = "4"
        updates.append('cylinder_count')
    else:
        valueInput = adsk.core.ValueInput.createByString("4")
        userParams.add('cylinder_count', valueInput, '', 'From SysML: numberOfCylinders')
        updates.append('cylinder_count (created)')

    # bore -> bore_diameter
    param = userParams.itemByName('bore_diameter')
    if param:
        param.expression = "86 mm"
        updates.append('bore_diameter')
    else:
        valueInput = adsk.core.ValueInput.createByString("86 mm")
        userParams.add('bore_diameter', valueInput, 'mm', 'From SysML: bore')
        updates.append('bore_diameter (created)')

    # stroke -> stroke_length
    param = userParams.itemByName('stroke_length')
    if param:
        param.expression = "86 mm"
        updates.append('stroke_length')
    else:
        valueInput = adsk.core.ValueInput.createByString("86 mm")
        userParams.add('stroke_length', valueInput, 'mm', 'From SysML: stroke')
        updates.append('stroke_length (created)')

    # headDiameter -> valve_head_dia
    param = userParams.itemByName('valve_head_dia')
    if param:
        param.expression = "30 mm"
        updates.append('valve_head_dia')
    else:
        valueInput = adsk.core.ValueInput.createByString("30 mm")
        userParams.add('valve_head_dia', valueInput, 'mm', 'From SysML: headDiameter')
        updates.append('valve_head_dia (created)')

    # threadSize -> spark_thread_size
    param = userParams.itemByName('spark_thread_size')
    if param:
        param.expression = "14 mm"
        updates.append('spark_thread_size')
    else:
        valueInput = adsk.core.ValueInput.createByString("14 mm")
        userParams.add('spark_thread_size', valueInput, 'mm', 'From SysML: threadSize')
        updates.append('spark_thread_size (created)')

    # crankRadius -> crank_radius
    param = userParams.itemByName('crank_radius')
    if param:
        param.expression = "43 mm"
        updates.append('crank_radius')
    else:
        valueInput = adsk.core.ValueInput.createByString("43 mm")
        userParams.add('crank_radius', valueInput, 'mm', 'From SysML: crankRadius')
        updates.append('crank_radius (created)')

    # length -> conrod_length
    param = userParams.itemByName('conrod_length')
    if param:
        param.expression = "144 mm"
        updates.append('conrod_length')
    else:
        valueInput = adsk.core.ValueInput.createByString("144 mm")
        userParams.add('conrod_length', valueInput, 'mm', 'From SysML: length')
        updates.append('conrod_length (created)')

    if updates:
        app.userInterface.messageBox(
            f'Updated {len(updates)} parameters:\n' + '\n'.join(updates))