function Get-Results {
  param ( $SrchStr )
  $SrchStr = "distinguishedName=" + $SrchStr
  $Searcher.filter=$SrchStr
  $Result = $Searcher.FindAll()
  [System.Collections.ArrayList]$Enum= @()
  Foreach($obj in $Result)
  {
    if( $obj.Properties.member )
    {
      Foreach($mem in $obj.Properties.member)
      {
        $Enum.Add($mem)
      }
    }
    if( $obj.Properties.objectclass -contains "group" )
    {
      write-host "Group Name: " $obj.Properties.name
      write-host "Group Members: " $obj.Properties.member
      write-host "Distinguished Name: " $obj.Properties.distinguishedname
      Write-Host "------------------------"
    }
  }
  if( $Enum )
  {
    Foreach($mem in $Enum)
    {
      Get-Results -SrchStr $mem
    }
  }
}

$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = ($domainObj.PdcRoleOwner).Name
$SearchString = "LDAP://"
$SearchString += $PDC + "/"
$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName

$Searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]$SearchString)
$objDomain = New-Object System.DirectoryServices.DirectoryEntry
$Searcher.SearchRoot = $objDomain
Get-Results -SrchStr "CN=Secret_Group,OU=CorpGroups,DC=corp,DC=com"
