import csv
import pandas as pd
import requests
from urllib import parse
from requests.exceptions import ConnectionError, TooManyRedirects, ReadTimeout

"""
Reads in the URL list. Generates a csv file of URLs and their http code when 
attempts made to reach URL. Saves to ./responses.csv.
"""


def main():
    """"""
    df = get_df_from_csv("./data/outcomes_software_urls.csv")
    url_list = get_urls(df)

    """
    for url in url_list:
        if url == "missing":
            print("missing")
        else:
            response = check_url(url)
            print(response[0], response[1])
            responses.append(response)
    with open("responses.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(responses)
    """

    categories = []
    for url in url_list:
        cat = url, analyse_keywords_in_url(url)
        categories.append(cat)
    with open("cats.csv", "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(categories)


def analyse_keywords_in_url(url: str):
    institutional_group = ["http://spindynamics.org"]
    institutional = [
        "http://t-stor.teagasc.ie/bitstream/11019/380/1/berry_imputation.pdf",
        "http://psrg.org.uk",
        "http://hdl.handle.net/10871/36891",
        ".ac.uk",
        "https://soft-dev.org",
        "https://doi.org/10.5523/bris.2s1zavsbkctna2bnh6g6os9n2k",
        "https://doi.org/10.15131/shef.data.13713598.v1",
        "http://bio.dei.unipd.it",
        "http://cvssp.org",
        "https://doi.org/10.17863/CAM.281",
        "https://drops.dagstuhl.de/opus",
    ]
    international_institutional = [
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
    public_commercial_code_repo = [
        "http://maximilian.strangeloop.co.uk",
        "sf.net",
        "github",
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
    public_openscience_repo = ["osf.io"]
    publisher = [
        "sagepub" "https://doi.org/10.1007/978-3-030-80439-8_13",
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
        "" "http://hts.sp.nitech.ac.jp",
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
    web_app = [
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
    preprint_site = ["arxiv", "/www.biorxiv.org/", "https://doi.org/10.1101/481754"]
    software_paper = ["joss.theoj.org", "https://doi.org/10.21105/joss.02043"]
    discipline_software_repo = [
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
        "http://apps.cytoscape.org/apps/slimscape",
        "https://www.food4rhino.com/",
    ]
    commercial_website = [
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
        "http://seabedhabitats.org",
        "http://hotventscoldocean.blogspot.co.uk",
        "https://www.statalist.org/forums/",
        "https://www.mail-archive.com",
        "https://www.agisoft.com/forum/",
        "https://pds.group/ava-clastics/",
        "https://medium.com/",
    ]
    conference_site = [
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
    uk_govt_software = ["http://ekn.defra.gov.uk"]
    internations_public_govt = [
        "https://sohowww.nascom.nasa.gov/solarsoft/radio/lofar/",
        "https://lambda.gsfc.nasa.gov/",
    ]  # with code
    search_site = ["scholar.google."]
    personal_site = [
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

    inappropriate = ["http://extasy-project.org", "http://rmox.net/"]

    news_blog = ["http://eyeonearth.org"]

    google_doc = ["http://goo.gl/VJKoBw"]

    unresponsive = [
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
        "drive.google",
        "http://goo.gl/NOnpmf",
        "http://purl.oclc.org/NET/cudaMap",
    ]
    data_platform = ["http://datadryad.org", "http://gigadb.org/"]

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
        if any([x in url for x in web_app]):
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
