# Implementation of the class SimulateInterface for the Battery

from Abstraction.SimulateInterface import SimulateInterface


class Simu1(SimulateInterface):

    def simula(self, config, **kwargs):

        # estat de carrega inicial de la bateria en Kw
        estat_bateria = config['cap_actual']  # estat inicial
        bat_max = config['bat_max']
        bat_min = config['bat_min']
        efficiency = config['efficiency']
        calendar = config['calendar']
        active_calendar = config['active_calendar'].copy()

        kw_carrega = []  # estat de carrega de la bateria al final de cada hora.
        consumption_profile = []
        cost_total = 0
        hora = 0

        for potencia in calendar:  # per cada hora del dia

            if potencia > 0:  # carreguem
                # gastem 30 Kw de xarxa pero en guardem a la bateria 30*0.9
                estat_bateria += (potencia * efficiency)

            elif potencia < 0:  # descarreguem
                # donem a xarxa 30Kw pero en realitat descarreguem 30
                estat_bateria += potencia

            cost = 0
            # comprovem si el que ens han fet fer ho podiem fer o si en fer-ho quedem fora els limits permesos
            if estat_bateria > bat_max:  # si sobre limit
                if hora == 0:
                    calendar[hora] = bat_max - estat_bateria  # actual - anterior
                else:
                    calendar[hora] = bat_max - kw_carrega[hora - 1]  # actual - anterior

                cost = estat_bateria - bat_max
                estat_bateria = bat_max

            elif estat_bateria < bat_min:  # si sota limit
                if hora == 0:
                    calendar[hora] = bat_min - estat_bateria  # actual - anterior
                else:
                    calendar[hora] = bat_min - kw_carrega[hora-1]  # actual - anterior

                cost = bat_min - estat_bateria
                estat_bateria = bat_min

            # Guardem el perfil de la bateria tot i que no es necessari, per visualitzar es util
            kw_carrega.append(estat_bateria)
            consumption_profile.append(potencia)
            hora += 1
            cost_total += cost  # TODO: Evaluar si va bé o no tornar el cost d'aproximacio d'un valor valid a la bateria

        consumption_profile_24h = [0.0] * 24  # format to 24h simulation
        for hora in range(len(consumption_profile)):
            index = active_calendar[0] + hora
            consumption_profile_24h[index] += consumption_profile[hora]

        return_dictionary = {'consumption_profile': consumption_profile_24h,
                             'consumed_Kwh': kw_carrega,
                             'cost_aproximacio': cost_total
                             }

        return return_dictionary
        # podriem fer que el cost fos la diferencia de correcions pero de moment hem decidit que no cal
        # perfil de la carrega de la bateria, estat final de carrega de la bateria
