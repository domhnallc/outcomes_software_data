import csv
import pandas as pd
import requests
from urllib import parse
from requests.exceptions import ConnectionError, TooManyRedirects, ReadTimeout
import helper as hlp

"""
Reads in the URL list. Generates a csv file of URLs and their http code when 
attempts made to reach URL. Saves to ./responses.csv.
"""
input_data_folder = "./jul23_data"
output_results_folder = "./jul23_output"

url_input_csv = f"{input_data_folder}/outcomes_software_urls.csv"


def main():

    df = get_df_from_csv(url_input_csv)
    url_list = get_urls(df)
    check_urls_for_http_response(url_list)
    categorise_urls(url_list)

def check_urls_for_http_response(url_list)
    
    for url in url_list:
        if url == "missing":
            print("missing")
        else:
            response = check_url(url)
            print(response[0], response[1])
            responses.append(response)
    with open("responses.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Url","Response"])
        writer.writerows(responses)
    

def check_urls_for_2xx_responses()
    # redo this with only the 2xx responses
    df_only_http200s = get_df_from_csv("./data/responses.csv")
    print(df_only_http200s)
    df_only_http200s = df_only_http200s.loc[
        (df_only_http200s["response"] == "200")
        | (df_only_http200s["response"] == "202")
    ]
    print(df_only_http200s)
    # df.loc[df['column_name'] == some_value]

    url_list = df_only_http200s["url"]

    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open("cats_only_200.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def categorise_urls(url_list):
    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open(f"{output_results_folder}/categorized_urls.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def analyse_keywords_in_url(url: str):
    institutional_group = [
        "https://ctiuk.org/projects/cogstack/",
        "https://braindynamicslab.org/code/",
        "http://spindynamics.org",
        "soft-dev.org",
        "http://www.arg-tech.org",
        "www.bioinf.org.uk",
    ]
    institutional = [
        "http://www.spass-prover.org/",
        "http://www.biospi.org",
        "http://t-stor.teagasc.ie/bitstream/11019/380/1/berry_imputation.pdf",
        "http://psrg.org.uk",
        "http://hdl.handle.net/10871/36891",
        ".ac.uk",
        "https://doi.org/10.5523/bris.2s1zavsbkctna2bnh6g6os9n2k",
        "https://doi.org/10.15131/shef.data.13713598.v1",
        "http://cvssp.org",
        "https://doi.org/10.17863/CAM.281",
    ]
    international_institutional = [
        "http://bio.dei.unipd.it",
        "https://drops.dagstuhl.de/opus",
        "inria.fr",
        "http://paccanarolab.org",
        "http://lat.inf.tu-dresden.de/",
        "http://nso.narit.or.th",
        ".edu",
        "http://fair.dei.unipd.it",
        "https://www.georgeinstitute.org/",
        "http://bioinfo.utu.fi",
        "https://hesperia.gsfc.nasa.gov/ssw/packages/xray/idl/f_thick_warm.pro",
    ]

    # e.g. confluence
    commercial_workspace_wiki = ["https://commons.lbl.gov/display/bisicles/BISICLES"]

    # not necessarily for sale, but held by a commercial site (like nvidia)
    public_commercial_code_repo = [
        "http://www.w3id.org/sdpo/",
        "https://developer.nvidia.com/",
        "https://dev.azure.com/hexstudios/ViveProjectionMapping",
        "https://commons.lbl.gov/display/bisicles/BISICLES",
        "codeocean.com",
        "http://maximilian.strangeloop.co.uk",
        "sf.net",
        "github.com",
        "bitbucket",
        "sourceforge",
        "gitlab",
        "code.google",
        "googlecode",
        "dylan.sf.net",
    ]
    public_noncommercial_archive_repo = [
        "zenodo",
        "figshare",
        "https://doi.org/10.17862/cranfield.rd.c.3292031",
    ]
    public_noncommercial_package_repo = [
        "https://anaconda.org/",
        "http://www.taverna.org.uk",
        "http://www.eclipse.org",
        "https://crates.io/",
        "hackage",
        "CRAN.R-project.org",
        "r-project",
        "mathworks",
        "openstack.org",
        "pypi.python.org",
        "https://plugins.qgis.org",
        "libraries.io",
        "pypi.org",
        "https://extensions.sketchup",
    ]
    public_openscience_repo = ["osf.io", "http://www.iplantcollaborative.org"]
    publisher = [
        "https://aip.scitation.org",
        "http://www.stata-journal.com",
        "http://www.llcsjournal.org/",
        "http://www.ifs.org.uk",
        "http://www.earth-surf-dynam.net/4/655/2016/",
        "sagepub",
        "https://doi.org/10.1007/978-3-030-80439-8_13",
        "https://doi.org/10.1007/978-3-319-96151-4_27",
        "https://doi.org/10.1007%2Fs11222-020-09966-2",
        "https://doi.org/10.1016/j.cageo.2007.11.007",
        "https://doi.org/10.1038/s41467-020-14545-0",
        "https://doi.org/10.1038/s41564-017-0063-9",
        "https://doi.org/10.1093/nar/gkz1234",
        "https://doi.org/10.1109/tmi.2021.3056023",
        "https://doi.org/10.1145/3377930.3390150",
        "https://doi.org/10.1242/jcs.161786",
        "https://doi.org/10.1364/BOE.10.001329",
        "oxfordjournals.org",
        "sciencedirect",
        "researchgate",
        "thelancet",
        "tandfonline",
        "dx.doi.org/10",
        "wiley.com",
        "pubs.acs.org",
        "nature.com",
        "https://www.stata-journal.com",
        "ncbi.nlm.nih.gov/pubmed",
        "https://www.ncbi.nlm.nih.gov",
        "mdpi.com",
        "https://www.jneurosci.org",
        "https://www.imcce.fr/",
        "https://www.icevirtuallibrary.com/doi/pdf/10.1680/jenge.18.00032",
        "https://www.geosci-model-dev.net/11/4215/2018/",
        "https://www.frontiersin.org",
        "https://www.earth-surf-dynam.net/",
        "www.degruyter.com",
        "https://www.aclweb.org/",
        "https://www.aanda.org/",
        "https://wellcomeopenresearch.org/",
        "https://royalsocietypublishing.org",
        "rsc.org",
        "ncbi.nlm.nih.gov",
        "peerj.com",
        "opg.optica.org",
        "iop.org",
        "springer.com",
        "oup.com",
        "biomedcentral.com",
        "journals.plos.org",
        "ieeexplore.ieee.org",
        "f1000research",
        "elifesciences.org" "j.cageo.",
        "j.cpc.",
        "j.cub",
        "j.envsoft",
        "j.ssnmr.",
        "acs.jcim",
        "acsomega",
        "journal.pone",
        "10.3390/",
        "https://doi.org/10.1007/978-3-030-80439-8_12",
        "dl.acm.org",
        "http://dev.biologists.org/",
        "https://earth-planets-space.springeropen.com/articles/10.1186/s40623-015-0332-x",
        "elifesciences.org/",
    ]
    documentation_site = ["readthedocs"]
    software_specific_website = [
        "github.io",
        "http://www.nmr-titan.com",
        "https://docs.lightkurve.org/index.html",
        "https://degiacomi.org/software/biobox/",
        "https://degiacomi.org/software/jabberdock/",
        "https://cadabra.science",
        "http://www.zsl.org/science/software/colony",
        "http://www.w3id.org/ep-plan",
        "http://www.vlfeat.org/matconvnet/",
        "http://www.transsys.net/",
        "http://www.tractor-mri.org.uk",
        "http://www.swiftsim.com/",
        "http://www.sequenceserver.com",
        "http://www.rsgislib.org",
        "http://www.rightfield.org.uk",
        "http://www.psics.org",
        "http://www.pamguard.org/",
        "http://www.order-n.org/",
        "http://www.openbsd.org/",
        "http://www.netlib.org/numeralgo/",
        "http://www.molpro.net",
        "http://www.mettel-prover.org",
        "http://www.menpo.org/",
        "http://www.seek4science.org",
        "https://biosimspace.org",
        "http://www.prismmodelchecker.org/",
        "http://www.ldak.org",
        "http://www.labtrove.org",
        "http://www.k-wave.org",
        "http://www.isale-code.de",
        "http://www.insectvision.org/3d-reconstruction-tools/habitat3d",
        "http://www.incompact3d.com",
        "http://www.hande.org.uk/",
        "http://www.gridcarbon.uk/",
        "http://www.grchombo.org",
        "http://www.geomorphology.com",
        "http://www.genomehubs.org",
        "http://www.gaussianprocess.org/gpml/code",
        "http://www.gap-system.org/",
        "http://www.flamegpu.com",
        "http://www.fitbenchmarking.com",
        "http://www.firedrakeproject.org",
        "http://www.extremetomato.com/projects/graphcoll/",
        "http://www.evosuite.org",
        "http://www.empiricalimaging.com",
        "http://www.dune-project.org",
        "http://www.dual.sphysics.org",
        "http://www.digtrace.co.uk",
        "http://www.deft-whois.org/",
        "http://www.defensivejs.com/",
        "http://www.dandeliion.com",
        "http://www.crystal.unito.it/index.php",
        "http://www.cpl-library.org",
        "http://www.cp2k.org",
        "http://www.copasi.org",
        "http://www.condatis.org.uk",
        "http://www.cistools.net",
        "http://www.chemshell.org",
        "http://www.channotation.org",
        "http://www.channelcoast.org",
        "http://www.cemrg.co.uk/software/cemrgapp.html",
        "http://www.ccalc.org.uk/",
        "http://www.bonej.org",
        "http://www.bone-finder.com",
        "http://www.biopepa.org",
        "http://www.biolayout.org/",
        "http://www.bempp.org",
        "http://www.avenirhealth.org/software-spectrum",
        "http://www.animalsimulation.org",
        "http://www.africanfarmergame.org/",
        "http://wwpdb.org/validation/validation-reports",
        "http://workcraft.org",
        "http://w3id.org/mqtt-plan",
        "http://tinyurl.com/9dhhgqj",
        "http://tiny.uzh.ch/dm",
        "http://thetisproject.org/",
        "http://tessa.tools/",
        "http://sleepful.me/download",
        "http://search.cpan.org/~ggallone/Bio-Homology-InterologWalk/",
        "http://scip.zib.de",
        "http://sbml.org/Software/JSBML",
        "http://savara.jboss.org/",
        "http://rivet.hepforge.org",
        "http://reaction-networks.net/control/",
        "http://radar-base.org",
        "http://purl.org/td/transportdisruption",
        "http://prismmodelchecker.org/games/",
        "http://phpsemantics.org",
        "http://page.mi.fu-berlin.de/cbenzmueller/leo/",
        "http://oss.deltares.nl/web/xbeach/home",
        "http://osnt.org/",
        "http://OpenSAFELY.org",
        "http://ompl.kavrakilab.org/",
        "http://not.yet.com",
        "http://natverse.org/",
        "http://naomi.unaids.org",
        "http://logiciels.pierrecouprie.fr/?page_id=402",
        "http://www.gwoptics.org/finesse/",
        "http://www.optados.org",
        "https://amplemr.wordpress.com/",
        "http://www.onetep.org",
        "https://irl.itch.io/narupaxr",
        "https://interactml.com/",
        "https://infobiotics.org",
        "https://idris-lang.org",
        "https://h1jet.hepforge.org/",
        "https://goat.genomehubs.org/",
        "https://fenicsproject.org/",
        "https://fat-forensics.org/",
        "https://eventerneuro.netlify.app/",
        "https://dune-project.org/modules/dune-composites/",
        "https://dual.sphysics.org",
        "http://lepbase.org/source-code/",
        "http://inlabru.org/",
        "http://isa-tools.org/",
        "http://hts.sp.nitech.ac.jp",
        "http://hermit-reasoner.com/",
        "http://geokey.org.uk/",
        "http://flagellarcapture.com/",
        "http://fenicsproject.org",
        "http://fathmm.biocompute.org.uk/",
        "https://extasy.readthedocs.io/en/latest/",
        "http://elmerice.elmerfem.org/",
        "http://easyhg.org/",
        "http://dynamorio.org/",
        "www.dynamomd.com",
        "dolfin-adjoint.org",
        "http://docs.pyro.ai/en/stable/contrib.oed.html",
        "https://cytag.corcencc.org",
        "https://www.cp2k.org/",
        "http://cowl.ws",
        "http://cosmologist.info/cosmomc/",
        "http://camb.info/",
        "http://bugseng.com/products/ppl",
        "http://blobtoolkit.genomehubs.org/",
        "http://bioblox.org/",
        "http://ansurr.com",
        "http://ambermd.org",
        "https://doi.org/10.5286/software/euphonic",
        "castep.org",
        "jalview",
        "https://zoonproject.wordpress.com/",
        "https://www.syncphonia.co.uk/",
        "https://www.simdynamics.org",
        "sharetrace.org",
        "https://www.seamlesswave.com/Flood_Human_ABM.html",
        "https://www.safetoolbox.info",
        "pyfr.org",
        "https://www.pybamm.org/",
        "https://www.prime-project.org/prime-framework-application-and-platform-agnostic-runtime-management-that-enables-portability-of-runtime-management-approaches/",
        "https://www.poppunk.net",
        "https://www.poets-project.org/tools/",
        "https://www.pcas.xyz",
        "https://www.onetep.org/Main/HomePage",
        ".nektar.info",
        "https://www.mr-startrack.com/",
        "https://www.mcs.anl.gov/petsc/petsc-current/docs/manualpages/PC/PCPATCH.html",
        "lammps",
        "https://www.ifs.org.uk/publications/8331",
        "https://www.idris-lang.org/",
        "https://www.cosmos.esa.int/",
        "https://www.code-saturne.org",
        "https://www.chemshell.org",
        "https://www.channelcoast.org",
        "https://www.amidine.net",
        "https://www.aftermath-tracing.com/",
        "https://workcraft.org",
        "https://tesarrec.web.app",
        "https://taverna.incubator.apache.org/",
        "https://siremol.org",
        "qtechtheory",
        "https://quantum-kite.com/",
        "https://qiskit.org/",
        "https://pixstem.org",
        "https://onetep.org/",
        "https://metawards.org",
        "https://laura.hepforge.org",
        "http://constraintmodelling.org",
        "http://firedrakeproject.org",
        "http://fluidity-project.org",
        "site.google.com",
        "http://atomap.org/index.html",
        "http://beehave-model.net/",
        "https://keigoimai.info/session-ocaml/",
        "sites.google.com",
    ]
    web_app_or_db = [
        "https://caginstability.ml",
        "http://www.zoompast.org",
        "http://www.tdmx.eu/",
        "http://www.pds.group/ava-clastics",
        "http://www.marinespecies.org",
        "https://biomodelanalyzer.org/",
        "http://www.epigraphdb.org/",
        "http://www.compadre-db.org",
        "http://www.cerealsdb.uk.net/cerealgenomics/CerealsDB/select_QTL.php",
        "http://shiny90.unaids.org",
        "http://plants.ensembl.org",
        "https://Jmleaglacio.users.earthengine.app/view/rgi7alphareviewerv001",
        "https://jackolney.shinyapps.io/ShinyCascade/",
        "http://emboeditor.herokuapp.com/",
        "http://cellcycle.org.uk/static/PPSIM/timecourse.html",
        "https://www.s3eurohab.eu/portal/",
        "https://w3id.org/",
        "http://biomodelanalyzer.org/",
        "http://blog.debroglie.net/strategies/",
        "http://brandmaier.de/shiny/sample-apps/SimLCS_app/",
        "http://ecohairandbeauty.com/virtual-salon",
    ]
    patent = [
        "https://www.ipo.gov.uk/p-ipsum/Case/ApplicationNumber/",
        "google.com/patents",
    ]
    project_or_consortium = [
        "https://digitalinclusiontoolkit.org/",
        "https://amt4oceansatflux.org/",
        "https://ai.biennial.com/#howitworks",
        "https://4273pi.org",
        "http://yoyomachines.io",
        "http://www.weavingcommunities.org/about/software",
        "http://www.vroracle.co.uk/",
        "http://www.urban-futures.org",
        "http://www.uk-pbc.com/resources/tools/riskcalculator/",
        "http://www.taxvis.org.uk/content/page/applications",
        "http://www.shelfseasmodelling.org",
        "http://www.serpentproject.com",
        "http://www.refugees.ai",
        "http://www.OpenPMU.org",
        "openpmu",
        "http://www.moorsforthefuture.org.uk",
        "repidemicsconsortium",
        "http://www.prime-project.org",
        "http://www.magic-air.uk",
        "http://www.cposs.org.uk/",
        "http://www.ccpsas.org/",
        "http://www.acceleratar.uk/",
        "http://tropics.blogs.ilrt.org/",
        "http://solidityproject.com",
        "http://projectglobalview.blogspot.co.uk/",
        "http://performancewithoutbarriers.com/vrinstrument/",
        "http://mycoast-project.org/",
        "http://ska-sdp.org",
        ".ecmwf.int",
        "https://projects.coin-or.org/oBB/",
        "https://kclhi.org/provenance",
        "https://hoys.space/",
        "https://gtr.ukri.org/projects?ref=EP%2FV051555%2F1",
        "https://grassroots.tools",
        "https://glennmasson.com/hdx-ms-resources-people-programs-papers/",
        "https://friction.org.uk/slippy-software/",
        "http://maptraits.wordpress.com/software/",
        "http://jermontology.org/",
        "http://ico2s.org",
        "http://eiis.co.uk/",
        "http://dryproject.co.uk/",
        "http://distributedcomponents.net/",
        "http://discoslastdance.blogspot.co.uk/",
        "http://digital-realism.net/2015/06/10/visualisation-toolkit/",
        "http://darecollaborative.net/2015/03/11/playing-beowulf-gaming-the-library/",
        "http://cumecs2012.blogspot.co.uk/",
        "https://www.itrc.org.uk/highlights/popnation-predicts-household-distribution-to-incredible-level-of-detail/",
        "https://www.i-sense.org.uk/",
        "https://www.dynahealth.eu/",
        "https://www.databoxproject.uk",
        "ligo.org/",
        "https://spiqe.co.uk",
        "https://www.ecmwf.int/",
        "https://sociam.org/",
        "https://sites.google.com/site/",
        "https://outofbounds.digital/#/resources",
        "https://mapper.gcrf-breccia.com/",
        "https://grassroots.tools/",
        "https://doi.pangaea.de/10.1594/PANGAEA.929749",
        "http://changingoceans2012.blogspot.co.uk/",
        "https://cometinitiative.org/DelphiManager/",
        "observablehq.com",
    ]  # doesnt link to software, just
    preprint_site = ["arxiv", "biorxiv.org", "https://doi.org/10.1101/481754"]
    software_paper = ["joss.theoj.org", "https://doi.org/10.21105/joss.02043"]
    discipline_software_repo = [
        "https://ascl.net/",
        "http://www.timeseriesclassification.com",
        "http://www.mybiosoftware.com",
        "http://www.coin-or.org/projects/oBB.xml",
        "http://www.bionode.io",
        "http://vallico.net/casinoqmc",
        "http://tools.epidemiology.net",
        "http://sccs-studies.info",
        "http://mloss.org/",
        "openmicroscopy.org",
        "http://bx-community.wikidot.com/examples:home",
        "https://www.bioconductor.org",
        "https://www.vaccineimpact.org",
        "https://www.openmicroscopy.org",
        "https://openep.io",
        "http://www.siremol.org",
        "bioconductor.org",
        "econpapers.repec.org/software/",
        "ideas.repec.org/",
        "http://ascl.net/1803.008",
    ]
    discipline_non_software_repo = [
        "http://thespace.org",
        "http://www.optimization-online.org",
        "http://www.integratedmodelling.org",
        "http://www.incisenet.org/",
        "http://inspirehep.net/record/1520002",
        ".iacr.org",
        "siam.org",
        "https://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000245",
    ]
    video = ["youtu.be", "youtube", "vimeo"]
    social_media = ["twitter.com"]
    commercial_appstore = [
        "unrealengine",
        "play.google.com",
        "itunes.apple.com",
        "softonic",
    ]
    non_commercial_appstore = [
        "https://app-movement.com",
        "http://apps.cytoscape.org/apps/slimscape",
        "https://www.food4rhino.com/",
    ]
    commercial_website = [
        "http://www.manageplaces.com/",
        "http://www.wtjohnson.co.uk/",
        "http://www.ravenscience.com",
        "http://www.quantemol.com",
        "https://www.manageplaces.com/",
        "http://www.ondex.org",
        "http://www.niab.com/",
        "http://www.lstm.co.uk",
        "http://www.lets-explore.com",
        "http://www.iotdatabox.com",
        "http://www.ihs.com/info/st/e/smartpm.aspx",
        "http://www.esa-da.org/content/finding-representativity-error",
        "http://www.e3me.com",
        "http://www.articulateinstruments.com/",
        "http://simpleware.com/software/physics-modules/",
        "https://hybridgifting.com/",
        "https://epic337255300.wordpress.com/our-product/",
        "http://keyfort.co.uk/solutions/software/freightvista",
        "http://fullscaledynamics.com/software/",
        "http://business.liftshare.com/",
        "https://www.tobiipro.com",
        "https://www.retinize.com/",
        "https://www.pricemyers.com/news/price--myers-launch-embodied-carbon-software-panda-52",
        "https://www.kisanhub.com/",
        "https://www.echoview.com/",
        "https://www.dnvgl.com/",
        "https://www.cognizant.com",
        "https://www.ansys.com/en-gb/products/fluids/ansys-fluent",
        "https://www.airqo.net/",
        "https://saturnsoftware2.co.uk",
        "safecap",
        "https://limitstate3d.com/peregrine",
        "https://leatonhydrogeology.com/",
        "accelrys.com",
        "k-plan.io",
        "https://entos.ai/qcore",
        "http://bela.io",
    ]
    forum_mailing_list_blog = [
        "http://www.sciencedaily.com/",
        "http://www.rna-seqblog.com/",
        "http://www.gridqtl.org.uk",
        "http://seabedhabitats.org",
        "http://hotventscoldocean.blogspot.co.uk",
        "https://www.statalist.org/forums/",
        "https://www.mail-archive.com",
        "https://www.agisoft.com/forum/",
        "https://pds.group/ava-clastics/",
        "https://medium.com/",
    ]
    conference_site = [
        "https://conferences.sigcomm.org/acm-icn/2018/proceedings/icn18posterdemo-final4.pdf",
        "http://proceedings.asmedigitalcollection.asme.org",
        "http://papers.nips.cc",
        "http://openaccess.thecvf.com/",
        "https://www.stata.com/meeting/uk18/",
        "https://www.ndss-symposium.org",
        "supercomputing.org",
        "https://proceedings.mlr.press",
        "meetingorganizer.copernicus.org",
    ]
    uk_public_govt_news = [
        "http://publications.naturalengland.org.uk/",
        ".nhs.uk",
        "https://www.gov.uk/hiv-overall-prevalence",
        "https://www.gov.uk/government/statistics/hiv-annual-data-tables"
        "https://www.gov.uk/government/publications/hiv-in-the-united-kingdom",
        "https://letstalkparks.co.uk",
        "www.gov.uk/government",
    ]  # with no links to software
    uk_govt_software = ["http://ekn.defra.gov.uk", "https://code.metoffice.gov.uk/"]
    internations_public_govt = [
        "http://www.osti.gov/",
        "https://sohowww.nascom.nasa.gov/solarsoft/radio/lofar/",
        "https://lambda.gsfc.nasa.gov/",
    ]  # with code
    search_site = ["scholar.google."]
    personal_site = [
        "http://www.tom-ridge.com",
        "http://www.louisaslett.com/",
        "http://www.laurenceanthony.net/",
        "http://www.derczynski.com",
        "http://www.danielerotolo.com/#!medliner/cid7",
        "http://www.coxphysics.com",
        "http://www.code.daniel-williams.co.uk/minke/",
        "http://rtaylor-essex.droppages.com",
        "http://muxviz.net",
        "http://mmcheng.net/dss/",
        "http://www.pierrecouprie.fr/",
        "http://kurlin.org",
        "http://gabrielegan.com/",
        "https://paulsbond.co.uk",
        "https://luweiyang.com/",
        "http://constantinou.info",
        "http://davidbekaert.com/",
        "hannahfry.co.uk",
        "http://louismccallum.com",
    ]
    non_software_website = [
        "http://earlymusictheory.org/Tinctoris",
        "https://ecohairandbeauty.com/virtual-salon/",
    ]

    inappropriate = [
        "http://extasy-project.org",
        "http://rmox.net/",
        "http://www.transforming-musicology.org/tools/metaMuSAK/",
    ]

    news_blog = ["http://eyeonearth.org"]

    google_doc = ["http://goo.gl/VJKoBw"]

    # includes where the parent website exists, but the webpage doesnt (i.e. not necessarily a 404)
    # or where the domain is back up for sale, so no 404 either
    # includes 1x login-walled that cannot be determined
    unresponsive = [
        "https://dev.xr4all.eu/product/calibration-method-mecm/",
        "http://www.quantmedia.org/coling2014/",
        "http://www.theibest.org/Life%20Cycle%20Sustainability%20Assessment%20(LCSA)%20-%20end%20of%20project%20report.pdf",
        "http://ekn.defra.gov.uk",
        "https://docs.lightkurve.org/api/lightkurve.seismology.Seismology.html",
        "https://docs.heliopy.org/en/stable/index.html",
        "https://dashboard.dev.minder.care/",
        "https://deft.limsi.fr/2015/corpus/train/TRAIN_TWEETS_ID-03042015.zip",
        "https://deft.limsi.fr/2015/tools/evaldeft2015_20150513.tar.gz",
        "https://deft.limsi.fr/2015/tools/evaldeft2015_20150513.tar.gz",
        "https://deft.limsi.fr/2015/tools/tweet_basic-retriever.zip",
        "https://deft.limsi.fr/2015/corpus/train/TRAIN_TWEETS_ID-03042015.zip",
        "https://creators.woodworks.org.uk/",
        "https://bit.ly/3vVJUOr",
        "https://biodynamo.web.cern.ch/",
        "https://biodynamo.org",
        "https://bananex.org/2020/03/04/toward-a-global-banana-map/",
        "http://www.xrayfels.co.uk",
        "http://www.wikilinkify.com",
        "http://www.who.int/malaria/publications/atoz/9789241507028/en/",
        "http://www.veritygos.org",
        "http://www.uni-muenster.de/InMind/",
        "http://www.ukcomes.org/codes",
        "http://www.tensornetworktheory.org",
        "http://www.tarquin.sourcefourge.net",
        "http://www.springsustainability.org/",
        "http://www.smokefreehomes.network",
        "http://www.scribble.org/",
        "http://www.renishaw.com/go/en/craniomaxillofacial-implants-and-software--42111",
        "http://www.pureintrawise.org/",
        "http://www.proteosuite.org",
        "http://www.proteoannotator.org/",
        "http://www.plantcell.org/content/27/4/1018.full",
        "http://www.phenoimageshare.org",
        "http://www.perellonieto.com/PyCalib/",
        "http://www.peano-framework.org/index.php/peano-v-3/",
        "http://www.paulodowd.com/2017/02/image-texture-processing.html",
        "http://www.osteolytica.com/",
        "http://www.openpermis.info",
        "http://www.omicanalytics.com/products/proteolabels/",
        "http://www.noninvasive.med.tohoku.ac.jp/ShidaharaLab/SFSRR.html",
        "http://www.nucleome.com",
        "http://www.muscleproject.org/",
        "http://www.mokapot.xyz",
        "http://www.missingdata.org.uk",
        "http://www.mecourse.com/landinig/software/threshgrad/threshgrad.html",
        "http://www.mechanochemistry.org/mcainsh/software.php",
        "https://cemmapswl.blog/",
        "http://www.urban-climate.net/",
        "http://www.sixthsensetransport.com/",
        "http://www.lifemirror.org/",
        "http://www.killerfungus.org",
        "http://www.jstarverifier.org",
        "http://www.itrc.org.uk/nismod/#.WMbLiH8qtdg",
        "http://www.inclusivedesigntoolkit.com/betterdesign2",
        "http://www.iearth.org.au/codes/",
        "http://www.handyurbansolutions.com",
        "http://www.gowsb.com",
        "http://www.gec-bas.info/",
        "http://www.footmiles.org",
        "http://www.esciencecentral.co.uk/",
        "http://www.dnald.org/",
        "http://www.dflybrain.org/GainControlModel.html",
        "http://vallico.new/casinoqmc",
        "http://www.dflybrain.org/FrequencyDomainMethods.html",
        "http://www.deepearthobservation.com",
        "http://www.datafax.com/software/idatafax/",
        "http://www.cossan.co.uk/software/open-cossan-engine.php",
        "http://www.constituencyexplorer.org.uk/explore/2015_election_results",
        "http://www.coastalme.org.uk",
        "http://www.click2go.umip.com/i/software/Biomedical_Software/TroGen.html",
        "http://www.boscorf.org/instruments/corewall",
        "http://www.acousticsensing.co.uk/",
        "http://vprover.org",
        "http://utopiadocs.com",
        "http://tytra.org.uk/",
        "http://tidal.lurk.org",
        "http://tapas-h2020.eu/results/",
        "http://staff.aist.go.jp/w.shinoda/MPDyn/index.html",
        "http://spiers-software.org/index.htm",
        "http://recomp.org.uk",
        "http://play-fair.uksouth.cloudapp.azure.com/?uid=137966&n-frames=10",
        "http://parafem.org.uk/news/general/179-geometric-and-material-nonlinearity",
        "http://orcahub.dsmynas.com:30000/orcahub/wp1/orb-slam/tree/raluca_dvl_integration",
        "http://octopus-code.org/wiki/Libxc",
        "http://oceans11.lanl.gov/cism/",
        "http://mio.pytheas.univ-amu.fr/~nencioli/research.php?type=eddy_detection",
        "http://metexplore.toulouse.inra.fr/joomla3/index.php",
        "http://dynamomd.org",
        "http://www.masssmappy.org",
        "http://mio.pytheas.univ-amu.fr/~doglioli/spasso.html",
        "http://www.latfield.org/",
        "http://TurkVolc.com",
        "http://www.sixthsensetransport.com/mobile-apps/wsb-mobile-app/",
        "https://www.attachment-monitor.org.uk/",
        "https://www.digitalthreads.co.uk/software",
        "http://125.22.91.149:5050/MemberLogin.aspx#b",
        "http://52.202.219.239:8080/",
        "http://52.202.219.239:8080/",
        "http://aninternetofsoftthings.com/an-introduction-to-arduino-micro-controllers/",
        "http://aninternetofsoftthings.com/capacitive-sensor-development-board/",
        "http://aninternetofsoftthings.com/files/2017/03/IoST-Networking-Infrastructure.pdf",
        "http://aninternetofsoftthings.com/photon-control-of-a-mosfet/",
        "http://aninternetofsoftthings.com/photon-publish-and-subscription-events/",
        "http://aninternetofsoftthings.com/summary-of-network-topologies/",
        "http://cfpm.org/ToRealSim/models",
        "http://cheart.co.uk",
        "http://clasp.gu.se/about/people/shalom-lappin/smog",
        "http://cometinitiative.org/DelphiManager/",
        "http://cp2k.org",
        "http://cx.tools",
        "http://cx.tools",
        "http://cytag.corcencc.org",
        "http://datadryad.org/resource/doi:10.5061/dryad.4gt8g",
        "http://directtrace.org/",
        "http://directtrace.org/",
        "http://docs.heliopy.org/en/stable/",
    ]

    cloud_filestore = [
        "https://bit.ly/36biSbh",
        "drive.google",
        "http://goo.gl/NOnpmf",
        "http://purl.oclc.org/NET/cudaMap",
    ]
    data_platform = [
        "datadryad.org",
        "http://gigadb.org/",
        "https://contribute.data.humancellatlas.org/",
    ]

    if url == "missing":
        return "missing"

    if not url == "missing" or not url == "None":
        if any([x in url for x in discipline_non_software_repo]):
            return "discipline-specific (non-software repo)"
        if any([x in url for x in uk_govt_software]):
            return "UK Govt Software Link"
        if any([x in url for x in non_software_website]):
            return "Non-software website"
        if any([x in url for x in unresponsive]):
            return "Non-responsive"
        if any([x in url for x in cloud_filestore]):
            return "Cloud filestore"
        if any([x in url for x in data_platform]):
            return "Data platform"
        if any([x in url for x in institutional]):
            return "institutional"
        if any([x in url for x in international_institutional]):
            return "international_institutional"
        if any([x in url for x in public_commercial_code_repo]):
            return "public_commercial_code_repo"
        if any([x in url for x in public_noncommercial_archive_repo]):
            return "public_noncommercial_archive_repo"
        if any([x in url for x in public_noncommercial_package_repo]):
            return "public_noncommercial_package_repo"
        if any([x in url for x in publisher]):
            return "publisher"
        if any([x in url for x in documentation_site]):
            return "documentation_site"
        if any([x in url for x in software_specific_website]):
            return "software_specific_website"
        if any([x in url for x in preprint_site]):
            return "preprint_site"
        if any([x in url for x in software_paper]):
            return "software_paper"
        if any([x in url for x in discipline_software_repo]):
            return "discipline_software_repo"
        if any([x in url for x in public_openscience_repo]):
            return "public openscience repo"
        if any([x in url for x in web_app_or_db]):
            return "web app"
        if any([x in url for x in patent]):
            return "patent"
        if any([x in url for x in project_or_consortium]):
            return "project or consortium"
        if any([x in url for x in video]):
            return "video"
        if any([x in url for x in social_media]):
            return "social media"
        if any([x in url for x in commercial_appstore]):
            return "commercial appstore"
        if any([x in url for x in non_commercial_appstore]):
            return "non-commercial appstore"
        if any([x in url for x in commercial_website]):
            return "commercial website"
        if any([x in url for x in forum_mailing_list_blog]):
            return "forum, mailinglist, blog"
        if any([x in url for x in conference_site]):
            return "conference site"
        if any([x in url for x in uk_public_govt_news]):
            return "UK Govt Public site"
        if any([x in url for x in internations_public_govt]):
            return "International public govt"
        if any([x in url for x in search_site]):
            return "search site"
        if any([x in url for x in personal_site]):
            return "personal website"
        if any([x in url for x in inappropriate]):
            return "inappropriate"
        if any([x in url for x in news_blog]):
            return "news_blog"
        if any([x in url for x in google_doc]):
            return "google_doc"
        if any([x in url for x in institutional_group]):
            return "institutional_group"
        if any([x in url for x in commercial_workspace_wiki]):
            return "commercial_workspace_wiki"

        else:
            return "unknown"


def get_df_from_csv(csv_to_read: str) -> pd.DataFrame:
    """Returns dataframe from a csv

    Args:
        csv_to_read (str): filepath of csv

    Returns:
        Dataframe: df
    """
    with open(csv_to_read) as data_in:
        df = pd.read_csv(data_in).fillna("missing")

    return df


def get_urls(df_in: pd.DataFrame) -> list:
    urls_list = []
    for url in df_in.Url:
        urls_list.append(url)

    return urls_list


def check_url(url: str):
    hostname = get_hostname_from_url(url)
    headers = {
        "Host": hostname,
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Referer": hostname,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        return url, r.status_code

    except ConnectionError:
        return url, "ConnectionError"
    except TooManyRedirects:
        return url, "TooManyRedirectsError"
    except ReadTimeout:
        return url, "ReadTimeoutError"


def get_hostname_from_url(url: str) -> str:
    """Returns hostname from a url e.g pure.qub.ac.uk

    Args:
        url (str): url to break down

    Returns:
        str: hostname
    """
    try:
        hostname = parse.urlsplit(url).hostname
    except AttributeError:
        hostname = "error"
    return hostname


if __name__ == "__main__":
    main()
