from data_warehouse import models
from . import crawler


def get_annual_regression_data(A, B):
    Recs = models.AnnualRecord.objects.values(A, B)
    dataMat = []
    labelMat = []
    for rec in Recs:
        dataMat.append([1.0, rec.get(A)])
        labelMat.append(rec.get(B))
    return dataMat, labelMat


def read_all_region_profile():
    """ Read out all regional profiles that are used for data crawling. """
    recs = []
    objs = models.Regions.objects.all()
    for obj in objs:
        name = obj.name
        url = obj.resource_url
        resource_type = obj.resource_type
        present_type = obj.resource_present_type
        recs.append((name, url, resource_type, present_type))
    return recs


def save_region_profile(rname, rtype, rptype, url):
    """ Save user posted regional profile to database. """
    RPs = models.Regions.objects.all()
    success = True
    RTN = 'SUCCESS'
    RegProf = models.Regions(name=rname,
                             resource_type=rtype.upper(),
                             resource_present_type=rptype,
                             resource_url=url)

    if RPs:
        for obj in RPs:
            if obj.name==rname and obj.resource_url==url:
                RTN = "Duplicated input!"
                success = False
                break
        if success:
            try:
                RegProf.save()
            except Exception as e:
                success = False
                RTN = 'Submitted data is of invalid format'
    else:
        try:
            RegProf.save()
        except Exception as e:
            success = False
            RTN = 'Submitted data is of invalid format'
    if success:
        return ('OK', RTN)
    else:
        return ('ERROR', RTN)


def crawl_and_save_data(rg, url, resource_type, order):
    """
    The function will crawl raw data from the specified URL
    and, according the raw data presented format (ranked or
    ordered) to download the raw data. The raw data is
    afterwards parsed into a canonical format that can be
    suitable for database population.
    """
    status, content = crawler.crawl_data(url, order)    
    if status=='ERROR':
        return (status, content)
    else:
        Labels = content[0]
        Data = content[1:]
        if order=='ORDERED':
            for D in Data:
                DataSet = [V for V in zip(Labels, D)]
                YL, YV = DataSet[0]
                AnnualDataSet = DataSet[1:-5]
                SeasonDataSet = DataSet[-5:]
                save_annual_data(rg, YV, resource_type, AnnualDataSet)
                save_season_data(rg, YV, resource_type, SeasonDataSet)
        return ('OK', 'Success')


# The following two functions should be futher refactored into one template
# based function.

def save_annual_data(rg, YV, resource_type, AnnualDataSet):
    """ Saving/Updating parased annual temperature records. """
    for ML, MV in AnnualDataSet:
        Recs = models.AnnualRecord.objects.filter(region=rg,
                                                  year=YV,
                                                  month=ML)
                        
        if not Recs:
            MaxTempV = None
            MinTempV = None
            MeanTempV = None
            SunshineV = None
            RainfallV = None
            RaindaysV = None
            DAFV = None
            if resource_type=='MAX':
                MaxTempV = MV
            if resource_type=='MIN':
                MinTempV = MV
            if resource_type=='MEN':
                MeanTempV = MV
            if resource_type=='SSN':
                SunshineV = MV
            if resource_type=='RNF':
                RainfallV = MV
            if resource_type=='RND':
                RaindaysV = MV
            if resource_type=='DAF':
                DAFV = MV
                        
            NewRec = models.AnnualRecord(
                region=rg,
                year=YV,
                max_temp=MaxTempV,
                min_temp=MinTempV,
                mean_temp=MeanTempV,
                sunshine=SunshineV,
                rainfall=RainfallV,
                raindays=RaindaysV,
                days_of_air_frist=DAFV,
                month=ML)
            NewRec.save()
        else:
            for obj in Recs:
                if resource_type=='MAX':
                    obj.max_temp = MV
                if resource_type=='MIN':
                    obj.min_temp = MV
                if resource_type=='MEN':
                    obj.mean_temp = MV
                if resource_type=='SSN':
                    obj.sunshine = MV
                if resource_type=='RND':
                    obj.raindays = MV
                if resource_type=='RNF':
                    RainfallV = MV
                if resource_type=='DAF':
                    DAFV = MV

                obj.save()


def save_season_data(rg, YV, resource_type, SeasonDataSet):
    """ Saving/Updating parased annual temperature records. """
    for ML, MV in SeasonDataSet:
        Recs = models.SeasonRecord.objects.filter(region=rg,
                                                  year=YV,
                                                  season=ML)
                        
        if not Recs:
            MaxTempV = None
            MinTempV = None
            MeanTempV = None
            SunshineV = None
            RainfallV = None
            RaindaysV = None
            DAFV = None
            if resource_type=='MAX':
                MaxTempV = MV
            if resource_type=='MIN':
                MinTempV = MV
            if resource_type=='MEN':
                MeanTempV = MV
            if resource_type=='SSN':
                SunshineV = MV
            if resource_type=='RNF':
                RainfallV = MV
            if resource_type=='RND':
                RaindaysV = MV
            if resource_type=='DAF':
                DAFV = MV
                        
            NewRec = models.SeasonRecord(
                region=rg,
                year=YV,
                max_temp=MaxTempV,
                min_temp=MinTempV,
                mean_temp=MeanTempV,
                sunshine=SunshineV,
                rainfall=RainfallV,
                raindays=RaindaysV,
                days_of_air_frist=DAFV,
                season=ML)
            NewRec.save()
        else:
            for obj in Recs:
                if resource_type=='MAX':
                    obj.max_temp = MV
                if resource_type=='MIN':
                    obj.min_temp = MV
                if resource_type=='MEN':
                    obj.mean_temp = MV
                if resource_type=='SSN':
                    obj.sunshine = MV
                if resource_type=='RND':
                    obj.raindays = MV
                if resource_type=='RNF':
                    RainfallV = MV
                if resource_type=='DAF':
                    DAFV = MV

                obj.save()
