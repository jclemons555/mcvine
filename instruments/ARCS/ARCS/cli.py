# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import click
from ..cli import instruments
from mcvine.cli import pyre_app, alias

cmd_prefix = "mcvine instruments arcs "

@instruments.group()
@alias("arcs", cmd_prefix)
def arcs():
    return

arcs_app = lambda name: pyre_app(parent=arcs, appname = name, cmd_prefix=cmd_prefix)

# beam sim
@arcs_app("arcs_analyze_beam")
def analyze_beam(ctx):
    from .applications import BeamAnalysis as mod
    return mod.App, mod.__file__

@arcs_app('arcs_moderator2sample')
def mod2sample(ctx):
    "moderator to sample simulation"
    from .applications import Moderator2Sample as mod
    return mod.App, mod.__file__

@arcs_app('arcs_m2s')
def m2s(ctx):
    "simplified moderator to sample simulation app"
    from .applications import M2S as mod
    return mod.App, mod.__file__

@arcs_app('arcs_beam')
def beam(ctx):
    "beam simulation. include mod2sample sim and post-processing"
    from .applications import Beam as mod
    return mod.App, mod.__file__


# detsys sim
@arcs.command(help="""convert scattereed neutrons to events (pixelID, tofChannelNo, prob)
intercepted by ARCS detector system.""")
@click.argument("neutrons", default="neutrons.dat")
@click.option("--workdir", default='work-arcs-neutrons2events')
@click.option("--nodes", default=0)
@click.option("--ncount", default=0)
@alias("arcs_neutrons2events", "%s neutrons2events" % cmd_prefix)
def neutrons2events(neutrons, workdir, nodes, ncount):
    from .applications.Neutrons2Events import run
    run(neutrons, workdir, nodes, ncount=ncount)
    return
    
@arcs.command(help="""convert events.dat (generated by neutrons2events) to nxs file""")
@click.argument("events", default="events.dat")
@click.argument("nxs", default="arcs-sim.nxs")
@click.option("--tofbinsize", default=0.1)
@click.option("--type", default="processed", type=click.Choice(['processed', 'raw']))
@click.option("--Ei", default=0., help="nominal incident energy in meV")
@alias("arcs_events2nxs", "%s events2nxs" % cmd_prefix)
def events2nxs(events, nxs, tofbinsize, type, ei):
    from .applications.Events2Nxs import run
    run(events, nxs, tofbinsize=tofbinsize, type=type, Ei=ei)
    return
    
@arcs.command(help="""convert scattereed neutrons to nexus file

Impl.: mcvine.instruments.ARCS.applications.Neutrons2Nxs
""")
@click.option("--neutrons", default="", help='path to neutron data file')
@click.option("--nxs", default="arcs-sim.nxs", help='nexus output path')
@click.option("--workdir", default='work-arcs-neutrons2nxs', help="working dir to save intermediate data fiels")
@click.option("--nodes", default=0)
@click.option("--type", default="raw", type=click.Choice(['processed', 'raw']))
@alias("arcs_neutrons2nxs", "%s neutrons2nxs" % cmd_prefix)
@click.pass_context
def neutrons2nxs(ctx, neutrons, nxs, workdir, nodes, type):
    if not neutrons:
        click.echo(ctx.get_help(), color=ctx.color)
        return
    from .applications.Neutrons2Nxs import run
    run(neutrons, nxs, type, workdir, nodes)
    return


# nexus file utilities
@arcs.group()
def nxs():
    "nexus utils"
    return

@nxs.command()
@click.option('--type', default="Ei", type=click.Choice(['Ei', 'monitor']), help='type of metadata')
@click.option('--beam_outdir', help='path to the output directory of arcs beam simulation')
@click.option('--nxs', help='path to the nexus file to be decorated')
@alias("arcs_nxs_populate_metadata", "%s nxs populate_metadata" % cmd_prefix)
@click.pass_context
def populate_metadata(ctx, type, beam_outdir, nxs):
    "populate metadata into the simulated nexus file"
    if not nxs or not beam_outdir:
        click.echo(ctx.get_help(), color=ctx.color)
        return
    from .applications import nxs as nxsmod
    f = getattr(nxsmod, "populate_%s_data" % type)
    f(beam_outdir, nxs)
    return

@nxs.command()
@click.argument("nxs")
@click.option('--out', default="iqe.nxs", help="output path. Eg. iqe.nxs")
@click.option('--use_ei_guess', default=False)
@click.option('--ei_guess', help='guess for Ei', default=0.)
@click.option('--qaxis', help='Qmin Qmax dQ', default=(0.,13.,0.1))
@click.option('--eaxis', help='Emin Emax dE', default=(0.,0.,0.))
@click.option('--tof2E/--no-tof2E', help='If true, input data must be tof events', default=True)
@alias("arcs_nxs_reduce", "%s nxs reduce" % cmd_prefix)
def reduce(nxs, out, use_ei_guess, ei_guess, qaxis, eaxis, tof2e):
    "run reduction"
    if ei_guess > 0:
        use_ei_guess = True

    qmin, qmax, dq = qaxis
    qaxis = (qmin, dq, qmax)
    
    import numpy as np
    if np.all(np.array(eaxis)==0.): eaxis = None
    if eaxis is not None:
        emin, emax, de = eaxis
        eaxis = emin, de, emax
    
    nxs = nxs.encode("utf8"); out = out.encode("utf8")
    print "* tof2E=%s" % tof2e
    d = dict(
        nxsfile = nxs,
        use_ei_guess = use_ei_guess,
        ei_guess = ei_guess,
        qaxis = qaxis,
        eaxis = eaxis,
        outfile = out,
        tof2E = tof2e,
        )
    from .applications.nxs import reduce
    reduce(**d)
    return


# End of file 
