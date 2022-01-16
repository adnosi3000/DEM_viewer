<style media="screen">
  img {width: 500px}
  table {border-collapse:collapse; border:1px solid black;}
  td {border: 1px solid black; padding: 4px;}
</style>

<h3>Simple DEM viewer</h3>
<p>This Python script allows one to visualize a <b>Digital Elevation Model</b>. Moreover, one can manipulate points that are displayed (zoom and rotation).
Data is presented in <code>pygame</code> window. To navigate use keyboard arrows (X and Y axis of the scene), ',' '.' keys (Z axis of the scene) and '+' '-' to zoom in and out.</p>
<p><img src="display.JPG" alt=""></p>
<p>DEM file should be represented as rows containing X, Y and Z values, eg.</p>
<p>
<table>
  <tr>
    <td>710828.00</td> <td>173254.00</td> <td>651.74</td>
  </tr>
  <tr>
    <td>710829.00</td> <td>173254.00</td> <td>651.77</td>
  </tr>
  <tr>
    <td>710830.00</td> <td>173254.00</td> <td>651.80</td>
  </tr>
  <tr>
    <td>...</td> <td>...</td> <td>...</td>
  </tr>
</table>
</p>
<p>Created using dependencies:
<ul>
  <li>pygame,</li>
  <li>numpy,</li>
  <li>random,</li>
  <li>math.</li>
</ul>
</p>
<p>Sample data attached as file .xyz</p>
